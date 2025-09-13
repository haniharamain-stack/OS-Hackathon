#!/usr/bin/env python3
"""
Nextcloud Talk Quote-of-the-Day Bot
Sends daily quotes to a Talk room and accepts user-submitted quotes
"""

import requests
import json
import random
import sqlite3
import schedule
import time
import logging
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NextcloudTalkBot:
    def __init__(self, nextcloud_url, username, password, room_token):
        self.base_url = nextcloud_url.rstrip('/')
        self.username = username
        self.password = password
        self.room_token = room_token
        self.auth = (username, password)
        self.quotes_db = 'quotes.db'
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for storing quotes"""
        conn = sqlite3.connect(self.quotes_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quote TEXT NOT NULL,
                author TEXT,
                category TEXT DEFAULT 'general',
                submitted_by TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add some default quotes if table is empty
        cursor.execute('SELECT COUNT(*) FROM quotes')
        if cursor.fetchone()[0] == 0:
            default_quotes = [
                ("The only way to do great work is to love what you do.", "Steve Jobs", "motivational"),
                ("Code is like humor. When you have to explain it, it's bad.", "Cory House", "programming"),
                ("In order to be irreplaceable, one must always be different.", "Coco Chanel", "motivational"),
                ("The best way to predict the future is to invent it.", "Alan Kay", "programming"),
                ("Life is what happens to you while you're busy making other plans.", "John Lennon", "funny"),
                ("I have not failed. I've just found 10,000 ways that won't work.", "Thomas Edison", "motivational"),
                ("Talk is cheap. Show me the code.", "Linus Torvalds", "programming"),
                ("The only impossible journey is the one you never begin.", "Tony Robbins", "motivational")
            ]
            
            for quote, author, category in default_quotes:
                cursor.execute('INSERT INTO quotes (quote, author, category) VALUES (?, ?, ?)',
                             (quote, author, category))
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def send_message(self, message):
        """Send message to Nextcloud Talk room"""
        url = f"{self.base_url}/ocs/v2.php/apps/spreed/api/v1/chat/{self.room_token}"
        
        headers = {
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/json',
        }
        
        data = {
            'message': message,
            'actorDisplayName': 'Quote Bot'
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, auth=self.auth)
            response.raise_for_status()
            logger.info(f"Message sent successfully: {message[:50]}...")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def get_random_quote(self, category=None):
        """Get a random quote from database"""
        conn = sqlite3.connect(self.quotes_db)
        cursor = conn.cursor()
        
        if category:
            cursor.execute('SELECT quote, author, category FROM quotes WHERE category = ? ORDER BY RANDOM() LIMIT 1', (category,))
        else:
            cursor.execute('SELECT quote, author, category FROM quotes ORDER BY RANDOM() LIMIT 1')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            quote, author, cat = result
            return f'💫 "{quote}"\n— {author} ({cat.title()})'
        else:
            return "No quotes found in the database."
    
    def add_quote(self, quote, author, category='general', submitted_by=None):
        """Add a new quote to database"""
        conn = sqlite3.connect(self.quotes_db)
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO quotes (quote, author, category, submitted_by) VALUES (?, ?, ?, ?)',
                      (quote, author, category, submitted_by))
        conn.commit()
        conn.close()
        
        logger.info(f"Added new quote by {author}")
        return f"✅ Quote added successfully!\n\"{quote}\" - {author}"
    
    def send_daily_quote(self):
        """Send the daily quote"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Rotate between different categories
        categories = ['motivational', 'programming', 'funny', 'general']
        category = random.choice(categories)
        
        quote = self.get_random_quote(category)
        message = f"🌅 **Quote of the Day** - {current_time}\n\n{quote}\n\n_Have a great day, team!_ 🚀"
        
        self.send_message(message)
    
    def check_for_commands(self):
        """Check for user commands in chat (simplified version)"""
        # In a real implementation, you'd poll the chat API for new messages
        # and parse commands like /addquote "text" "author" "category"
        pass
    
    def get_stats(self):
        """Get quote statistics"""
        conn = sqlite3.connect(self.quotes_db)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM quotes')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT category, COUNT(*) FROM quotes GROUP BY category')
        by_category = cursor.fetchall()
        
        conn.close()
        
        stats = f"📊 **Quote Bot Statistics**\n\nTotal quotes: {total}\n\nBy category:\n"
        for category, count in by_category:
            stats += f"• {category.title()}: {count}\n"
        
        return stats

def main():
    parser = argparse.ArgumentParser(description='Nextcloud Talk Quote Bot')
    parser.add_argument('--url', required=True, help='Nextcloud URL (e.g., http://localhost/nextcloud)')
    parser.add_argument('--username', required=True, help='Nextcloud username')
    parser.add_argument('--password', required=True, help='Nextcloud password')
    parser.add_argument('--room-token', required=True, help='Talk room token')
    parser.add_argument('--send-now', action='store_true', help='Send quote immediately')
    parser.add_argument('--add-quote', nargs=3, metavar=('QUOTE', 'AUTHOR', 'CATEGORY'), help='Add a new quote')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon with scheduled quotes')
    
    args = parser.parse_args()
    
    # Initialize bot
    bot = NextcloudTalkBot(args.url, args.username, args.password, args.room_token)
    
    if args.send_now:
        bot.send_daily_quote()
    elif args.add_quote:
        quote, author, category = args.add_quote
        result = bot.add_quote(quote, author, category)
        print(result)
    elif args.stats:
        stats = bot.get_stats()
        print(stats)
        bot.send_message(stats)
    elif args.daemon:
        # Schedule daily quote at 9 AM
        schedule.every().day.at("09:00").do(bot.send_daily_quote)
        
        print("Quote bot started! Scheduled to send daily quotes at 9:00 AM")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nBot stopped.")
    else:
        print("Use --help to see available options")

if __name__ == "__main__":
    main()
