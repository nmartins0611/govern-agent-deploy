# Global Cheeseburger Consumption Map

A simple web application that displays average cheeseburger consumption data on an interactive world map.

## Features

- Interactive world map using Leaflet.js
- Color-coded circles representing consumption levels
- Click on any country to see detailed consumption statistics
- Top 5 countries ranking
- Responsive design
- Pure HTML/CSS/JavaScript (no build process required)

## Files

- `index.html` - Main HTML page
- `style.css` - Styling and layout
- `data.js` - Cheeseburger consumption data for countries
- `app.js` - Map initialization and interactivity
- `README.md` - This file

## Deployment on Apache

### Option 1: Copy to Apache DocumentRoot

```bash
# Copy the application to Apache's web directory
sudo cp -r cheeseburger-map-app /var/www/html/

# Set proper permissions
sudo chown -R apache:apache /var/www/html/cheeseburger-map-app
sudo chmod -R 755 /var/www/html/cheeseburger-map-app
```

Access at: `http://your-server/cheeseburger-map-app/`

### Option 2: Create a Virtual Host

Create Apache config file: `/etc/httpd/conf.d/cheeseburger-map.conf`

```apache
<VirtualHost *:80>
    ServerName cheeseburger-map.example.com
    DocumentRoot /var/www/cheeseburger-map-app

    <Directory /var/www/cheeseburger-map-app>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    ErrorLog /var/log/httpd/cheeseburger-map-error.log
    CustomLog /var/log/httpd/cheeseburger-map-access.log combined
</VirtualHost>
```

Then:
```bash
# Copy files
sudo cp -r cheeseburger-map-app /var/www/

# Set permissions
sudo chown -R apache:apache /var/www/cheeseburger-map-app
sudo chmod -R 755 /var/www/cheeseburger-map-app

# Restart Apache
sudo systemctl restart httpd
```

### Option 3: Local Testing

For quick testing without Apache:

```bash
cd cheeseburger-map-app
python3 -m http.server 8000
```

Access at: `http://localhost:8000/`

## Requirements

- Apache 2.4+ (or any web server capable of serving static files)
- Modern web browser with JavaScript enabled
- Internet connection (for loading Leaflet.js library and map tiles from CDN)

## Data

The consumption data is fictional and for demonstration purposes only. Data includes:
- 35+ countries across all continents
- Consumption measured in cheeseburgers per person per year
- Population estimates

## Customization

### Update Data

Edit `data.js` to add/modify countries:

```javascript
{
    lat: 51.5074,
    lng: -0.1278,
    country: "Your Country",
    consumption: 50,
    population: "10M"
}
```

### Change Colors

Modify the `getColor()` function in `data.js` to adjust consumption level colors.

### Adjust Map Settings

In `app.js`, modify the initial view:

```javascript
const map = L.map('map').setView([latitude, longitude], zoomLevel);
```

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

## License

This is a demonstration application. Feel free to use and modify as needed.
