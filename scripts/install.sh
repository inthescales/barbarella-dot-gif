crontab -l > tmp
echo "0 */12 * * * sh /var/www/bots/barbarella-dot-gif/scripts/run" >> tmp
crontab tmp
