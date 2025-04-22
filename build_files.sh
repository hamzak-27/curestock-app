#!/bin/bash

# This script is used to build and prepare the public directory for Vercel deployment

# Exit immediately if a command exits with a non-zero status
set -e

echo "=== Starting build process ==="
echo "Current directory contents:"
ls -la

# Create and populate the public directory
echo "=== Setting up public directory ==="
mkdir -p public

# Copy existing staticfiles if they exist
if [ -d "staticfiles" ]; then
  echo "Copying existing staticfiles to public..."
  cp -r staticfiles/* public/ 2>/dev/null || true
fi

# Ensure minimum required static files exist
echo "=== Creating essential static files ==="

# Create index.html if it doesn't exist
if [ ! -f "public/index.html" ]; then
  cat > public/index.html << 'EOL'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CureStock App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>CureStock App</h1>
        <p>Static content is being served from the public directory.</p>
        <p>If you're seeing this page, your Vercel deployment is working correctly!</p>
    </div>
    <script src="script.js"></script>
</body>
</html>
EOL
  echo "Created index.html"
fi

# Create style.css if it doesn't exist
if [ ! -f "public/style.css" ]; then
  cat > public/style.css << 'EOL'
/* Basic styles */
body {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
  background-color: #f5f5f5;
  color: #333;
}

.container {
  width: 80%;
  max-width: 800px;
  margin: 30px auto;
  padding: 20px 30px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
  color: #3366cc;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

p {
  margin-bottom: 15px;
}
EOL
  echo "Created style.css"
fi

# Create script.js if it doesn't exist
if [ ! -f "public/script.js" ]; then
  cat > public/script.js << 'EOL'
// Simple script to confirm JavaScript is working
console.log('Vercel deployment is working correctly!');

document.addEventListener('DOMContentLoaded', function() {
  // Add a timestamp to show when the page was loaded
  const footer = document.createElement('footer');
  footer.style.textAlign = 'center';
  footer.style.marginTop = '30px';
  footer.style.color = '#666';
  footer.style.fontSize = '0.8rem';
  footer.innerHTML = `<p>Page loaded at: ${new Date().toLocaleString()}</p>`;
  document.body.appendChild(footer);
});
EOL
  echo "Created script.js"
fi

# Create a verification file
echo "Vercel deployment verification" > public/vercel.txt

echo "=== Public directory contents ==="
ls -la public/

# Try to install requirements and collect static files
echo "=== Installing Python requirements ==="
pip install --no-cache-dir -r vercel-requirements.txt || echo "Failed to install requirements, continuing..."

echo "=== Running collectstatic ==="
python manage.py collectstatic --noinput || echo "Collectstatic failed, continuing with existing static files..."

echo "=== Final public directory contents ==="
ls -la public/

echo "=== Build process completed ===" 