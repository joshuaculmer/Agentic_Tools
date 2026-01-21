#!/usr/bin/env bash
set -euo pipefail

TARGET_REL_PATH="../GUI"
mkdir -p "$TARGET_REL_PATH"
cd "$TARGET_REL_PATH"

echo "Initializing React + Vite + TypeScript boilerplate in $PWD..."

# Create Vite React-TS project
npm create vite@latest . -- --template react-ts

echo "Installing dependencies..."
npm install

# Add common React dependencies
echo "Adding additional dependencies..."
npm install react-router-dom
npm install --save-dev @types/react-router-dom

# The default Vite React-TS template already includes:
# - React 18+
# - TypeScript
# - Vite configuration
# - ESLint setup
# - Basic App component
# - Hot Module Replacement (HMR)

echo "✓ React + Vite + TypeScript boilerplate setup complete!"
echo ""
echo "Available commands:"
echo "  npm run dev       - Start development server"
echo "  npm run build     - Build for production"
echo "  npm run preview   - Preview production build"
echo "  npm run lint      - Run ESLint"
echo ""

# Open in VS Code
if command -v code >/dev/null 2>&1; then
  echo "Opening in VS Code..."
  code .
else
  echo "VS Code 'code' command not found."
  echo "Install VS Code and ensure 'code' is in your PATH to auto-open projects."
fi

echo ""
echo "To get started:"
echo "  cd $TARGET_REL_PATH"
echo "  npm run dev"
npm run dev
