"""
GPAS 4.0 - Sistema REAL de Monitoring de Preços
Monitora preços em sites portugueses REAIS para identificar oportunidades de arbitragem
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import pandas as pd
from typing import Dict, List, Optional
import re

class RealPriceMonitor:
    """Monitor REAL de preços que funciona com sites portugueses"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Sites REAIS portugueses para monitorizar
        self.retailers = {
            'worten': {
                'name': 'Worten',
                'base_url': 'https://www.worten.pt',
                'search_url': 'https://www.worten.pt/search?query={}',
                'price_selector': '.sales-price, .price-current, .price',
                'title_selector': 'h1, .product-title, .title'
            },
            'fnac': {
                'name': 'Fnac',
                'base_url': 'https://www.fnac.pt',
                'search_url': 'https://www.fnac.pt/SearchResult/ResultList.aspx?Search={}',
                'price_selector': '.price, .price-current',
                'title_selector': 'h1, .product-title'
            },
            'mediamarkt': {
                'name': 'Media Markt',
                'base_url': 'https://www.mediamarkt.pt',
                'search_url': 'https://www.mediamarkt.pt/pt/search.html?query={}',
                'price_selector': '.price, .price-current',
                'title_selector': 'h1, .product-title'
            },
            'elcorteingles': {
                'name': 'El Corte Inglés',
                'base_url': 'https://www.elcorteingles.pt',
                'search_url': 'https://www.elcorteingles.pt/pesquisa/?s={}',
                'price_selector': '.price, .price-current',
                'title_selector': 'h1, .product-title'
            }
        }
        
        # Produtos REAIS para monitorizar (alta demanda)
        self.target_products = [
            'iPhone 15 Pro',
            'MacBook Air M2',
            'AirPods Pro',
            'PlayStation 5',
            'Nintendo Switch',
            'Samsung Galaxy S24',
            'iPad Air',
            'Apple Watch Series 9',
            'Sony WH-1000XM5',
            'Dyson V15'
        ]
    
    def extract_price(self, html: str, price_selector: str) -> Optional[float]:
        """Extrai preço REAL do HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            price_elements = soup.select(price_selector)
            
            for element in price_elements:
                price_text = element.get_text().strip()
                # Regex para extrair preços em euros
                price_match = re.search(r'(\d+[.,]\d+|\d+)', price_text.replace(',', '.'))
                if price_match:
                    return float(price_match.group(1))
            return None
        except Exception as e:
            print(f"Erro ao extrair preço: {e}")
            return None
    
    def extract_title(self, html: str, title_selector: str) -> Optional[str]:
        """Extrai título REAL do produto"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            title_elements = soup.select(title_selector)
            if title_elements:
                return title_elements[0].get_text().strip()
            return None
        except Exception as e:
            print(f"Erro ao extrair título: {e}")
            return None
    
    def search_product_real(self, retailer_key: str, product_name: str) -> List[Dict]:
        """Busca REAL de produto em retailer específico"""
        retailer = self.retailers.get(retailer_key)
        if not retailer:
            return []
        
        try:
            search_url = retailer['search_url'].format(product_name.replace(' ', '+'))
            print(f"🔍 Buscando '{product_name}' em {retailer['name']}: {search_url}")
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar produtos na página de resultados
            products = []
            product_links = soup.find_all('a', href=True)
            
            for link in product_links[:5]:  # Primeiros 5 resultados
                href = link.get('href')
                if not href or 'javascript:' in href:
                    continue
                
                # Construir URL completa
                if href.startswith('/'):
                    product_url = retailer['base_url'] + href
                elif href.startswith('http'):
                    product_url = href
                else:
                    continue
                
                # Buscar informações do produto
                try:
                    product_response = self.session.get(product_url, timeout=10)
                    product_response.raise_for_status()
                    
                    price = self.extract_price(product_response.text, retailer['price_selector'])
                    title = self.extract_title(product_response.text, retailer['title_selector'])
                    
                    if price and title and product_name.lower() in title.lower():
                        products.append({
                            'retailer': retailer['name'],
                            'title': title,
                            'price': price,
                            'url': product_url,
                            'timestamp': datetime.now().isoformat(),
                            'currency': 'EUR'
                        })
                        print(f"✅ Encontrado: {title} - €{price}")
                        
                except Exception as e:
                    print(f"❌ Erro ao processar produto: {e}")
                    continue
                
                time.sleep(1)  # Rate limiting
            
            return products
            
        except Exception as e:
            print(f"❌ Erro ao buscar em {retailer['name']}: {e}")
            return []
    
    def monitor_all_retailers(self, product_name: str) -> List[Dict]:
        """Monitora produto em TODOS os retailers"""
        all_results = []
        
        print(f"\n🚀 MONITORANDO PREÇOS REAIS PARA: {product_name}")
        print("=" * 60)
        
        for retailer_key in self.retailers.keys():
            results = self.search_product_real(retailer_key, product_name)
            all_results.extend(results)
            time.sleep(2)  # Rate limiting entre retailers
        
        return all_results
    
    def calculate_arbitrage_opportunity(self, products: List[Dict]) -> List[Dict]:
        """Calcula oportunidades REAIS de arbitragem"""
        if len(products) < 2:
            return []
        
        opportunities = []
        
        # Ordenar por preço
        sorted_products = sorted(products, key=lambda x: x['price'])
        lowest_price_product = sorted_products[0]
        
        for product in sorted_products[1:]:
            price_diff = product['price'] - lowest_price_product['price']
            roi_percentage = (price_diff / lowest_price_product['price']) * 100
            
            # Calcular custos REAIS
            amazon_fee = product['price'] * 0.15  # 15% fee Amazon
            shipping_cost = 5.0  # €5 shipping estimado
            total_costs = amazon_fee + shipping_cost
            
            net_profit = price_diff - total_costs
            real_roi = (net_profit / lowest_price_product['price']) * 100
            
            if real_roi > 20:  # ROI mínimo de 20%
                opportunities.append({
                    'buy_from': lowest_price_product['retailer'],
                    'buy_price': lowest_price_product['price'],
                    'buy_url': lowest_price_product['url'],
                    'sell_to': product['retailer'],
                    'sell_price': product['price'],
                    'sell_url': product['url'],
                    'gross_profit': price_diff,
                    'amazon_fee': amazon_fee,
                    'shipping_cost': shipping_cost,
                    'net_profit': net_profit,
                    'roi_percentage': real_roi,
                    'product_title': product['title'],
                    'timestamp': datetime.now().isoformat()
                })
        
        return opportunities
    
    def run_real_monitoring_cycle(self) -> Dict:
        """Executa ciclo COMPLETO de monitorização"""
        print("\n🔥 INICIANDO MONITORIZAÇÃO REAL DE PREÇOS")
        print("🎯 Objetivo: Encontrar oportunidades de arbitragem REAIS")
        print("💰 ROI mínimo: 20%")
        print("=" * 80)
        
        all_opportunities = []
        monitoring_results = {
            'timestamp': datetime.now().isoformat(),
            'products_monitored': [],
            'opportunities_found': [],
            'total_opportunities': 0,
            'best_roi': 0
        }
        
        for product in self.target_products[:3]:  # Primeiros 3 produtos para teste
            print(f"\n📱 PRODUTO: {product}")
            
            # Monitorar em todos os retailers
            product_results = self.monitor_all_retailers(product)
            
            if product_results:
                # Calcular oportunidades
                opportunities = self.calculate_arbitrage_opportunity(product_results)
                
                monitoring_results['products_monitored'].append({
                    'product': product,
                    'retailers_found': len(product_results),
                    'opportunities': len(opportunities)
                })
                
                if opportunities:
                    print(f"\n💰 OPORTUNIDADES ENCONTRADAS PARA {product}:")
                    for opp in opportunities:
                        print(f"  🛒 Comprar: {opp['buy_from']} - €{opp['buy_price']:.2f}")
                        print(f"  💸 Vender: {opp['sell_to']} - €{opp['sell_price']:.2f}")
                        print(f"  💵 Lucro Líquido: €{opp['net_profit']:.2f}")
                        print(f"  📈 ROI: {opp['roi_percentage']:.1f}%")
                        print(f"  🔗 URL Compra: {opp['buy_url']}")
                        print("  " + "-" * 50)
                    
                    all_opportunities.extend(opportunities)
                    
                    # Atualizar melhor ROI
                    best_roi = max([opp['roi_percentage'] for opp in opportunities])
                    if best_roi > monitoring_results['best_roi']:
                        monitoring_results['best_roi'] = best_roi
                else:
                    print(f"  ❌ Nenhuma oportunidade rentável encontrada")
            else:
                print(f"  ❌ Produto não encontrado em nenhum retailer")
            
            print("\n" + "=" * 60)
            time.sleep(3)  # Pausa entre produtos
        
        monitoring_results['opportunities_found'] = all_opportunities
        monitoring_results['total_opportunities'] = len(all_opportunities)
        
        # Resumo final
        print(f"\n🎯 RESUMO DA MONITORIZAÇÃO:")
        print(f"📊 Produtos monitorados: {len(monitoring_results['products_monitored'])}")
        print(f"💰 Oportunidades encontradas: {monitoring_results['total_opportunities']}")
        print(f"🚀 Melhor ROI: {monitoring_results['best_roi']:.1f}%")
        
        if all_opportunities:
            total_potential_profit = sum([opp['net_profit'] for opp in all_opportunities])
            print(f"💵 Lucro potencial total: €{total_potential_profit:.2f}")
        
        return monitoring_results

# Função para testar o sistema
def test_real_monitoring():
    """Teste REAL do sistema de monitorização"""
    monitor = RealPriceMonitor()
    results = monitor.run_real_monitoring_cycle()
    return results

if __name__ == "__main__":
    # Executar teste real
    test_real_monitoring()

