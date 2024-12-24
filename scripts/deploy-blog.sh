#!/bin/bash

# Load environment variables
source .env

# Generate static files
cd frontend
npm run build

# Copy static files to blog directory
cp -r build/* ../blog/public/

# Deploy to GitHub Pages
cd ../blog
hexo deploy -g 