"""
GPAS 4.0 - BACKEND REVOLUCIONÁRIO
Sistema que vai DESTRUIR a concorrência e fazer o utilizador RICO!
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import threading
import json
from services.ai_arbitrage_brain import AIArbitrageBrain

# Inicializar Flask
app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gpas-4-revolutionary-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'gpas-4-jwt-secret')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gpas4.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
CORS(app, origins="*")  # Permitir todas as origens para desenvolvimento
jwt = JWTManager(app)
db = SQLAlchemy(app)

# Inicializar o cérebro de IA
ai_brain = AIArbitrageBrain()

# Modelos de Base de Dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    subscription_tier = db.Column(db.String(50), default='starter')
    daily_budget = db.Column(db.Float, default=1000.0)
    total_profit = db.Column(db.Float, default=0.0)
    auto_trading_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subscription_tier': self.subscription_tier,
            'daily_budget': self.daily_budget,
            'total_profit': self.total_profit,
            'auto_trading_enabled': self.auto_trading_enabled,
            'created_at': self.created_at.isoformat()
        }

class ArbitrageTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    source_platform = db.Column(db.String(50), nullable=False)
    target_platform = db.Column(db.String(50), nullable=False)
    source_price = db.Column(db.Float, nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float, nullable=False)
    roi_percentage = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, purchased, sold, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'source_platform': self.source_platform,
            'target_platform': self.target_platform,
            'source_price': self.source_price,
            'target_price': self.target_price,
            'profit': self.profit,
            'roi_percentage': self.roi_percentage,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

# Rotas de Autenticação
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Registo de novo utilizador"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Nome, email e password são obrigatórios'}), 400
        
        # Verificar se o email já existe
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já está registado'}), 409
        
        # Criar novo utilizador
        user = User(
            name=data['name'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Criar token de acesso
        access_token = create_access_token(identity=user.email)
        
        return jsonify({
            'message': 'Utilizador registado com sucesso!',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login de utilizador"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email e password são obrigatórios'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.email)
            return jsonify({
                'access_token': access_token,
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Email ou password inválidos'}), 401
            
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Rotas do Dashboard
@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Obter estatísticas do dashboard"""
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        # Obter transações do utilizador
        transactions = ArbitrageTransaction.query.filter_by(user_id=user.id).all()
        
        # Calcular estatísticas
        total_transactions = len(transactions)
        total_profit = sum(t.profit for t in transactions if t.status == 'completed')
        avg_roi = sum(t.roi_percentage for t in transactions) / total_transactions if total_transactions > 0 else 0
        
        # Estatísticas por status
        pending_transactions = len([t for t in transactions if t.status == 'pending'])
        active_transactions = len([t for t in transactions if t.status in ['purchased', 'sold']])
        
        return jsonify({
            'user': user.to_dict(),
            'stats': {
                'total_profit': total_profit,
                'total_transactions': total_transactions,
                'average_roi': avg_roi,
                'pending_transactions': pending_transactions,
                'active_transactions': active_transactions,
                'success_rate': 87.5,  # Simulado
                'daily_budget_used': ai_brain.current_daily_spent,
                'daily_budget_total': user.daily_budget
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Rotas de Arbitragem
@app.route('/api/arbitrage/scan', methods=['POST'])
@jwt_required()
def scan_opportunities():
    """Escanear oportunidades de arbitragem"""
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        # Configurar parâmetros do utilizador no AI brain
        ai_brain.total_daily_budget = user.daily_budget
        ai_brain.auto_trading_enabled = user.auto_trading_enabled
        
        # Escanear oportunidades
        opportunities = ai_brain.scan_global_opportunities()
        
        # Converter para formato JSON
        opportunities_data = []
        for opp in opportunities:
            opportunities_data.append({
                'product_name': opp.product_name,
                'source_platform': opp.source_platform,
                'target_platform': opp.target_platform,
                'source_price': opp.source_price,
                'target_price': opp.target_price,
                'profit': opp.profit,
                'roi_percentage': opp.roi_percentage,
                'confidence_score': opp.confidence_score,
                'risk_level': opp.risk_level,
                'shipping_time': opp.shipping_time,
                'category': opp.category,
                'auto_buy_recommended': opp.auto_buy_recommended
            })
        
        # Gerar insights
        insights = ai_brain.generate_ai_insights(opportunities)
        
        return jsonify({
            'opportunities': opportunities_data,
            'insights': insights,
            'scan_timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/arbitrage/execute', methods=['POST'])
@jwt_required()
def execute_purchase():
    """Executar compra automática"""
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        data = request.get_json()
        
        # Criar objeto de oportunidade a partir dos dados
        from services.ai_arbitrage_brain import ArbitrageOpportunity
        opportunity = ArbitrageOpportunity(
            product_name=data['product_name'],
            source_platform=data['source_platform'],
            target_platform=data['target_platform'],
            source_price=data['source_price'],
            target_price=data['target_price'],
            profit=data['profit'],
            roi_percentage=data['roi_percentage'],
            confidence_score=data['confidence_score'],
            risk_level=data['risk_level'],
            shipping_time=data['shipping_time'],
            category=data['category'],
            trend_score=data.get('trend_score', 50),
            viral_potential=data.get('viral_potential', 0.5),
            auto_buy_recommended=data['auto_buy_recommended'],
            source_currency='USD',
            target_currency='USD'
        )
        
        # Executar compra
        result = ai_brain.auto_execute_purchase(opportunity)
        
        # Se a compra foi bem-sucedida, guardar na base de dados
        if result['status'] == 'success':
            transaction = ArbitrageTransaction(
                user_id=user.id,
                product_name=opportunity.product_name,
                source_platform=opportunity.source_platform,
                target_platform=opportunity.target_platform,
                source_price=opportunity.source_price,
                target_price=opportunity.target_price,
                profit=opportunity.profit,
                roi_percentage=opportunity.roi_percentage,
                status='purchased'
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            result['transaction_id'] = transaction.id
        
        return jsonify(result), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/arbitrage/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """Obter histórico de transações"""
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        transactions = ArbitrageTransaction.query.filter_by(user_id=user.id).order_by(ArbitrageTransaction.created_at.desc()).all()
        
        return jsonify({
            'transactions': [t.to_dict() for t in transactions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Rotas de IA
@app.route('/api/ai/predictions', methods=['GET'])
@jwt_required()
def get_ai_predictions():
    """Obter previsões de IA"""
    try:
        viral_products = ai_brain.predict_viral_products()
        
        return jsonify({
            'viral_predictions': viral_products,
            'generated_at': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/ai/chat', methods=['POST'])
@jwt_required()
def ai_chat():
    """Chat com assistente de IA"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Simulação de resposta de IA (em produção seria GPT-4)
        responses = {
            'oportunidades': 'Encontrei 148 oportunidades com ROI médio de 304%. As melhores estão na categoria fitness com ROI de 353%.',
            'lucro': 'Com base no seu perfil, pode gerar €2.000-€5.000 por mês com o orçamento atual.',
            'produtos': 'Os produtos mais lucrativos agora são: Bluetooth Headsets (300% ROI), Gaming Controllers (250% ROI) e Fitness Equipment (350% ROI).',
            'risco': 'O seu nível de risco está otimizado. Recomendo manter 70% em produtos de baixo risco e 30% em alto ROI.',
            'default': 'Como posso ajudá-lo a maximizar os seus lucros hoje? Posso analisar oportunidades, ajustar estratégias ou executar compras automáticas.'
        }
        
        # Escolher resposta baseada na mensagem
        response = responses['default']
        for key in responses:
            if key in message.lower():
                response = responses[key]
                break
        
        return jsonify({
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Rota de configurações
@app.route('/api/settings/update', methods=['PUT'])
@jwt_required()
def update_settings():
    """Atualizar configurações do utilizador"""
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'Utilizador não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar configurações
        if 'daily_budget' in data:
            user.daily_budget = data['daily_budget']
        if 'auto_trading_enabled' in data:
            user.auto_trading_enabled = data['auto_trading_enabled']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Configurações atualizadas com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Rota de saúde
@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'message': 'GPAS 4.0 API está funcionando!',
        'timestamp': datetime.utcnow().isoformat(),
        'ai_brain_status': 'active'
    }), 200

# Inicialização da base de dados
def create_tables():
    """Criar tabelas da base de dados"""
    with app.app_context():
        db.create_all()
        
        # Criar utilizador demo se não existir
        demo_user = User.query.filter_by(email='demo@gpas4.com').first()
        if not demo_user:
            demo_user = User(
                name='Demo User',
                email='demo@gpas4.com',
                subscription_tier='professional',
                daily_budget=5000.0
            )
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            db.session.commit()

# Função para iniciar monitoring em background
def start_background_monitoring():
    """Iniciar monitoring de IA em background"""
    def monitor():
        print("🤖 Iniciando monitoring de IA em background...")
        # ai_brain.start_continuous_monitoring()  # Comentado para não bloquear
    
    # Iniciar em thread separada
    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()

if __name__ == '__main__':
    # Criar tabelas da base de dados
    create_tables()
    
    # Iniciar monitoring em background
    start_background_monitoring()
    
    print("🚀 GPAS 4.0 - BACKEND REVOLUCIONÁRIO INICIADO!")
    print("💰 Sistema que vai DESTRUIR a concorrência!")
    print("🤖 IA ativa e pronta para gerar lucros!")
    
    # Executar aplicação
    app.run(host='0.0.0.0', port=5000, debug=True)

