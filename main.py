import requests
import json
from typing import List, Dict
import os
import sys

class LiveDataSearcher:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def search_across_all_files(self, query: str) -> List[Dict]:
        """Search across all JSON files in real-time without downloading"""
        all_results = []
        query = query.lower().strip()
        
        print(f"\033[1;36m\n🔍 Searching for '{query}' ...\033[0m")
        
        for i in range(1, 13):
            url = f"{self.base_url}/data-{i}.json"
            try:
                # Fetch and search in real-time
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if isinstance(data, list):
                    # Search through this file's data
                    file_results = self.search_in_data(data, query)
                    all_results.extend(file_results)
                    
            except requests.exceptions.RequestException:
                # Skip files that can't be loaded
                continue
            except json.JSONDecodeError:
                # Skip files with invalid JSON
                continue
        
        return all_results
    
    def search_in_data(self, data: List[Dict], query: str) -> List[Dict]:
        """Search through a single dataset"""
        results = []
        
        for record in data:
            if (query in str(record.get('Name', '')).lower() or
                query in str(record.get('Number', '')).lower() or
                query in str(record.get('Carrier', '')).lower() or
                query in str(record.get('Address', '')).lower() or
                query in str(record.get('Email', '')).lower()):
                results.append(record)
        
        return results
    
    def display_results(self, results: List[Dict], query: str):
        """Display search results in a formatted way"""
        if not results:
            print(f"\033[1;31m\n❌ No results found for '{query}'.\033[0m")
            return
        
        print(f"\033[1;32m\n🎉 Found {len(results)} result(s) for '{query}':\033[0m")
        print("\033[1;35m" + "=" * 80 + "\033[0m")
        
        for i, record in enumerate(results, 1):
            print(f"\033[1;33mResult {i}:\033[0m")
            print(f"  \033[1;34mName:\033[0m    {record.get('Name', 'N/A')}")
            print(f"  \033[1;34mNumber:\033[0m  {record.get('Number', 'N/A')}")
            print(f"  \033[1;34mCarrier:\033[0m {record.get('Carrier', 'N/A')}")
            print(f"  \033[1;34mAddress:\033[0m {record.get('Address', 'N/A')}")
            print(f"  \033[1;34mEmail:\033[0m   {record.get('Email', 'N/A')}")
            print("\033[1;35m" + "-" * 80 + "\033[0m")
    
    def test_connection(self) -> bool:
        """Test if we can connect to at least one JSON file"""
        test_url = f"{self.base_url}/data-1.json"
        try:
            response = requests.get(test_url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def display_banner(self):
        """Display colorful banner"""
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = """
\033[1;35m

████████╗██████╗  █████╗ ███████╗███████╗██████╗ 
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
   ██║   ██████╔╝███████║███████╗█████╗  ██████╔╝
   ██║   ██╔══██╗██╔══██║╚════██║██╔══╝  ██╔══██╗
   ██║   ██║  ██║██║  ██║███████║███████╗██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
                Made By Sawwqib
                                                 
\033[0m
        """
        print(banner)
    
    def run(self):
        """Main interactive loop"""
        self.display_banner()
        
        print("\033[1;36mLoading ...\033[0m")
        
        # Test connection
        if not self.test_connection():
            print("\033[1;31m\n❌ Cannot connect to the database. Please check:\033[0m")
            print("   \033[1;33m- Internet connection\033[0m")
            print("   \033[1;33m- If database is accessible\033[0m")
            return
        
        print("\033[1;32m\n✅ Connection successful!\033[0m")
        print("\033[1;36m\n📋 You can search by: Name, Number or Email\033[0m")
        print("\033[1;33m💡 Type 'quit', 'exit', or press Ctrl+C to leave\033[0m")
        
        # Main search loop
        while True:
            try:
                print("\n" + "\033[1;35m" + "─" * 50 + "\033[0m")
                search_term = input("\033[1;36m\n🔍 Enter search term: \033[0m").strip()
                
                if search_term.lower() in ['quit', 'exit', 'q']:
                    print("\033[1;35m\n👋 Goodbye! Thank you for using Traser!\033[0m")
                    break
                
                if not search_term:
                    print("\033[1;31mPlease enter a search term.\033[0m")
                    continue
                
                # Perform live search
                results = self.search_across_all_files(search_term)
                self.display_results(results, search_term)
                
            except KeyboardInterrupt:
                print("\033[1;35m\n\n👋 Goodbye! Thank you for using Traser!\033[0m")
                break
            except Exception as e:
                print(f"\033[1;31mAn error occurred: {e}\033[0m")

def main():
    url_chars = [104, 116, 116, 112, 115, 58, 47, 47, 115, 99, 105, 110, 116, 105, 108, 108, 97, 116, 105, 110, 103, 45, 115, 116, 114, 117, 100, 101, 108, 45, 50, 55, 54, 54, 55, 48, 46, 110, 101, 116, 108, 105, 102, 121, 46, 97, 112, 112]
    base_url = ''.join(chr(c) for c in url_chars)
    
    searcher = LiveDataSearcher(base_url)
    searcher.run()

if __name__ == "__main__":
    main()