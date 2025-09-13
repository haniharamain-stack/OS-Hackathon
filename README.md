# Nextcloud Talk Quote Bot 🤖💫

A Python-based bot that sends daily inspirational quotes to your Nextcloud Talk rooms. Perfect for keeping your team motivated with quotes about programming, motivation, and life!

## Features

- 📅 **Daily Scheduled Quotes**: Automatically sends quotes at 9:00 AM
- 🗃️ **SQLite Database**: Stores quotes locally with categories and metadata
- 🎯 **Category Support**: Organizes quotes by type (motivational, programming, funny, general)
- 🔄 **Manual Control**: Send quotes on-demand or add new ones via command line
- 📊 **Statistics**: Track your quote collection with detailed stats
- 🚀 **Easy Setup**: Simple configuration and deployment

## Requirements

- Python 3.6+
- Nextcloud instance with Talk app installed
- Valid Nextcloud user account
- Talk room token

## Installation

1. **Download the project**:
   - **Option A**: Download ZIP file from the link above and extract it
   - **Option B**: Clone the repository:
     ```bash
     git clone https://github.com/your-username/nextcloud-quote-bot.git
     cd nextcloud-quote-bot
     ```

2. **Install required Python packages**:
   ```bash
   pip3 install requests schedule
   ```

3. **Make the script executable**:
   ```bash
   chmod +x quote_bot.py
   chmod +x run_daily_quote.sh
   ```

## Configuration

### Getting Your Room Token

1. Open your Nextcloud Talk room in a web browser
2. Look at the URL - it will be something like: `https://your-nextcloud.com/apps/spreed/room_token_here`
3. The room token is the part after `/room/` in the URL

### Setting Up Credentials

Edit `run_daily_quote.sh` to include your Nextcloud details:

```bash
#!/bin/bash
cd /path/to/your/quote_bot
python3 quote_bot.py \
  --url "https://your-nextcloud-url.com" \
  --username "your_bot_username" \
  --password "your_bot_password" \
  --room-token "your_room_token" \
  --send-now
```

## Usage

### Send Quote Immediately
```bash
python3 quote_bot.py --url "http://your-nextcloud" --username "bot_user" --password "bot_pass" --room-token "room_token" --send-now
```

Or use the shell script:
```bash
./run_daily_quote.sh
```

### Add a New Quote
```bash
python3 quote_bot.py --url "http://your-nextcloud" --username "bot_user" --password "bot_pass" --room-token "room_token" --add-quote "Your quote here" "Author Name" "category"
```

### View Statistics
```bash
python3 quote_bot.py --url "http://your-nextcloud" --username "bot_user" --password "bot_pass" --room-token "room_token" --stats
```

### Run as Daemon (Scheduled Daily Quotes)
```bash
python3 quote_bot.py --url "http://your-nextcloud" --username "bot_user" --password "bot_pass" --room-token "room_token" --daemon
```

## Automation

### Using Cron for Daily Quotes

Add to your crontab (`crontab -e`) to send daily quotes at 9:00 AM:

```bash
0 9 * * * /path/to/your/run_daily_quote.sh >> /var/log/quote_bot.log 2>&1
```

### Using Systemd (Linux)

Create a systemd service file `/etc/systemd/system/quote-bot.service`:

```ini
[Unit]
Description=Nextcloud Talk Quote Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/quote_bot
ExecStart=/usr/bin/python3 /path/to/quote_bot/quote_bot.py --url "http://your-nextcloud" --username "bot_user" --password "bot_pass" --room-token "room_token" --daemon
Restart=always

[Install]
WantedBy=multi-user.target
```

Then enable and start the service:
```bash
sudo systemctl enable quote-bot.service
sudo systemctl start quote-bot.service
```

## Quote Categories

The bot includes these default categories:
- **motivational**: Inspirational and uplifting quotes
- **programming**: Tech and coding-related quotes
- **funny**: Humorous and light-hearted quotes
- **general**: Miscellaneous life quotes

## Default Quotes

The bot comes pre-loaded with 8 inspiring quotes from notable figures like:
- Steve Jobs
- Cory House
- Coco Chanel
- Alan Kay
- John Lennon
- Thomas Edison
- Linus Torvalds
- Tony Robbins

## Database Structure

The SQLite database (`quotes.db`) stores:
- **id**: Unique quote identifier
- **quote**: The quote text
- **author**: Quote author
- **category**: Quote category
- **submitted_by**: Who added the quote (optional)
- **date_added**: When the quote was added

## Command Line Options

```
--url URL              Nextcloud URL (required)
--username USERNAME    Nextcloud username (required)
--password PASSWORD    Nextcloud password (required)
--room-token TOKEN     Talk room token (required)
--send-now            Send quote immediately
--add-quote QUOTE AUTHOR CATEGORY  Add a new quote
--stats               Show statistics
--daemon              Run as daemon with scheduled quotes
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**: 
   - Verify your username and password
   - Check if two-factor authentication is enabled (you may need an app password)

2. **Room Token Issues**:
   - Ensure the bot user has access to the Talk room
   - Double-check the room token from the URL

3. **Network Issues**:
   - Verify the Nextcloud URL is accessible
   - Check firewall settings

### Logging

The bot logs important events. To see logs when running as daemon:
```bash
journalctl -u quote-bot.service -f
```

## Security Notes

- Store credentials securely
- Consider using environment variables instead of hardcoding passwords
- Use app passwords if two-factor authentication is enabled
- Restrict file permissions on scripts containing credentials

## Contributing

Feel free to contribute by:
- Adding new quote categories
- Improving the message formatting
- Adding new features like user interaction commands
- Enhancing error handling

## License

This project is open source. Feel free to modify and distribute as needed.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Nextcloud Talk API documentation
3. Verify your Nextcloud and Talk app versions are compatible

---

**Enjoy spreading daily inspiration to your team!** 🌟
