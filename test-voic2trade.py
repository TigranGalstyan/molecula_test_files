#!/usr/bin/env python3
"""
Test script for n8n Voice-Activated Trading System

This script demonstrates how to test the n8n workflow endpoints
and shows the complete voice-to-trade functionality using Groq for free 
speech-to-text transcription and LLM parsing.
"""

import requests
import json
import time
from datetime import datetime

class N8nVoiceTradingTester:
    """Test client for n8n voice trading workflow"""
    
    def __init__(self, base_url):
        """
        Initialize the tester
        
        Args:
            base_url: Base URL of your n8n instance (e.g., 'https://your-n8n-instance.com')
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def test_voice_command(self, audio_url, user_id="test_user"):
        """
        Test voice command processing
        
        Args:
            audio_url: URL to audio file
            user_id: User identifier
            
        Returns:
            API response
        """
        url = f"{self.base_url}/webhook/voice-command"
        payload = {
            "audio_url": audio_url,
            "user_id": user_id
        }
        
        print(f"Testing voice command with audio: {audio_url}")
        response = self.session.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("-" * 50)
        
        return response.json()
    
    def test_balance(self, exchange="binance"):
        """
        Test balance retrieval
        
        Args:
            exchange: Exchange name (binance, coinbase)
            
        Returns:
            API response
        """
        url = f"{self.base_url}/webhook/balance"
        params = {"exchange": exchange}
        
        print(f"Testing balance retrieval for {exchange}")
        response = self.session.get(url, params=params)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("-" * 50)
        
        return response.json()
    
    def test_orders(self, exchange="binance"):
        """
        Test orders retrieval
        
        Args:
            exchange: Exchange name (binance, coinbase)
            
        Returns:
            API response
        """
        url = f"{self.base_url}/webhook/orders"
        params = {"exchange": exchange}
        
        print(f"Testing orders retrieval for {exchange}")
        response = self.session.get(url, params=params)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("-" * 50)
        
        return response.json()
    
    def test_no_audio_input(self):
        """
        Test voice command processing with no audio input
        
        Returns:
            API response
        """
        url = f"{self.base_url}/webhook/voice-command"
        payload = {
            "user_id": "test_user"
            # Missing audio_url field
        }
        
        print("Testing voice command with no audio input")
        response = self.session.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("-" * 50)
        
        return response.json()
    
    def test_empty_audio_url(self):
        """
        Test voice command processing with empty audio URL
        
        Returns:
            API response
        """
        url = f"{self.base_url}/webhook/voice-command"
        payload = {
            "audio_url": "",
            "user_id": "test_user"
        }
        
        print("Testing voice command with empty audio URL")
        response = self.session.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("-" * 50)
        
        return response.json()
    
    def test_malformed_request(self):
        """
        Test voice command processing with malformed request
        
        Returns:
            API response
        """
        url = f"{self.base_url}/webhook/voice-command"
        payload = {
            "invalid_field": "invalid_value",
            "another_invalid": 123
        }
        
        print("Testing voice command with malformed request")
        response = self.session.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("-" * 50)
        
        return response.json()
    
    def test_passing_error_response(self):
        """
        Test voice command processing that triggers error response nodes
        
        Returns:
            API response
        """
        url = f"{self.base_url}/webhook/voice-command"
        payload = {
            "audio_url": "https://github.com/TigranGalstyan/molecula_test_files/raw/refs/heads/main/non_trade.m4a",
            "user_id": "test_user"
        }
        
        print("Testing voice command that should trigger error response")
        print("Note: This tests the workflow's error handling paths")
        response = self.session.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("-" * 50)
        
        return response.json()

def demo_error_scenarios():
    """Demonstrate error handling scenarios"""
    
    # Initialize tester
    tester = N8nVoiceTradingTester("https://tigrann.app.n8n.cloud")
    
    print("\n🚨 Testing Error Scenarios")
    print("=" * 40)
    
    # Test error scenarios - keeping only main essential tests
    error_tests = [
        {
            "name": "No Audio Input",
            "test_method": tester.test_no_audio_input,
            "expected_error": "No audio input provided"
        },
        {
            "name": "Empty Audio URL",
            "test_method": tester.test_empty_audio_url,
            "expected_error": "No audio input provided"
        },
        {
            "name": "Malformed Request",
            "test_method": tester.test_malformed_request,
            "expected_error": "No audio input provided"
        },
        {
            "name": "Passing Error Response",
            "test_method": tester.test_passing_error_response,
            "expected_error": "Various error responses"
        }
    ]
    
    for i, test in enumerate(error_tests, 1):
        print(f"\n{i}. {test['name']}")
        print(f"   Expected: {test['expected_error']}")
        
        try:
            result = test['test_method']()
            
            if 'error' in result:
                print(f"   ✅ Error Caught: {result.get('error', 'Unknown error')}")
                if 'message' in result:
                    print(f"   📝 Message: {result.get('message')}")
            elif 'success' in result and not result['success']:
                print(f"   ✅ Error Handled: {result.get('message', 'Unknown error')}")
            else:
                print(f"   ⚠️ Unexpected Response: {result}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        time.sleep(1)  # Pause between requests
    
    print("\n✅ Error scenario testing completed!")

def demo_voice_commands():
    """Demonstrate various voice commands"""
    
    # Initialize tester (replace with your n8n URL)
    tester = N8nVoiceTradingTester("https://tigrann.app.n8n.cloud")
    
    print("🎤 Voice-Activated Trading System - n8n Demo")
    print("=" * 60)
    
    # Test voice commands with mock audio URLs
    voice_commands = [
        {
            "name": "Buy Bitcoin Market Order",
            "audio_url": "https://github.com/TigranGalstyan/molecula_test_files/raw/refs/heads/main/buy_btc_binance.m4a",
            "expected_transcription": "Buy 0.5 Bitcoin on Binance at market price"
        },
        {
            "name": "Sell Ethereum Limit Order",
            "audio_url": "https://github.com/TigranGalstyan/molecula_test_files/raw/refs/heads/main/sell_eth.m4a",
            "expected_transcription": "Sell 10 ETH at $3,200 on Coinbase"
        },
        {
            "name": "Buy Bitcoin Limit Order",
            "audio_url": "https://github.com/TigranGalstyan/molecula_test_files/raw/refs/heads/main/buy_btc_limit.m4a",
            "expected_transcription": "Place a limit order to buy 1 BTC at $45,000 on Binance"
        },
    ]
    
    print("\n📝 Testing Voice Commands")
    print("-" * 30)
    
    for i, command in enumerate(voice_commands, 1):
        print(f"\n{i}. {command['name']}")
        print(f"   Expected: '{command['expected_transcription']}'")
        
        try:
            result = tester.test_voice_command(command['audio_url'])
            
            if result.get('success'):
                print(f"   ✅ Success: {result.get('trade_summary', 'Command processed')}")
                if 'order_result' in result:
                    order = result['order_result']
                    print(f"   📊 Order: {order['side']} {order['quantity']} {order['symbol']} @ {order['price']}")
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        time.sleep(1)  # Pause between requests

def main():
    """Main demo function"""
    
    print("🎯 n8n Voice-Activated Trading System - Test Suite")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show different testing options
    print("\n🧪 Testing Options:")
    print("1. Run voice command tests (requires n8n instance)")
    print("2. Run error scenario tests")
    
    choice = input("\nSelect option (1-2) or press Enter to show info: ").strip()
    
    if choice == "1":
        demo_voice_commands()
    elif choice == "2":
        demo_error_scenarios()
    else:
        # Show info
        print("\n" + "=" * 60)
        print("To run the actual voice command and error tests:")
        print("1. Update the base_url in the script")
        print("2. Uncomment the test calls below")
        print("3. Run: python test-n8n-workflow.py")
        
        # Uncomment the lines below to run actual tests
        # demo_voice_commands()
        # demo_error_scenarios()

if __name__ == "__main__":
    main() 