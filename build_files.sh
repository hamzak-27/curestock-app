#!/bin/bash

# Build script for Vercel Django deployment
echo "Building the project..."

# Explicitly create staticfiles directory
mkdir -p staticfiles

# Install requirements
echo "Installing minimal requirements..."
pip install -r requirements-minimal.txt

# Create a placeholder file to ensure staticfiles exists
echo "This is a placeholder to ensure the staticfiles directory exists" > staticfiles/placeholder.txt
echo "Creating CSS file in staticfiles..."
cat > staticfiles/style.css << 'EOL'
/* Basic styles */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  line-height: 1.6;
}

.container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
}

/* Header styles */
header {
  background-color: #4b6cb7;
  color: white;
  padding: 1rem 0;
  text-align: center;
}

/* Footer styles */
footer {
  background-color: #f4f4f4;
  text-align: center;
  padding: 1rem 0;
  margin-top: 2rem;
}
EOL

echo "Build completed. Files in staticfiles directory:"
ls -la staticfiles/ 