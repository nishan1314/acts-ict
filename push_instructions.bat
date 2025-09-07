@echo off
echo ========================================
echo ACTS - GitHub Push Instructions
echo ========================================
echo.

echo Current Status:
echo ✅ Git repository initialized
echo ✅ Files committed successfully
echo ✅ Remote repository configured
echo.

echo Next Steps:
echo.
echo 1. If a login dialog appears, use your GitHub credentials
echo 2. If prompted for username: nishan1314
echo 3. If prompted for password: Use Personal Access Token (not password)
echo.
echo To create Personal Access Token:
echo - Go to: https://github.com/settings/tokens
echo - Click "Generate new token (classic)"
echo - Select scopes: repo, workflow
echo - Copy the token and use it as password
echo.

echo Manual Push Command:
echo git push -u origin main
echo.

echo Alternative: Use GitHub CLI
echo 1. Install GitHub CLI: https://cli.github.com/
echo 2. Run: gh auth login
echo 3. Run: git push -u origin main
echo.

echo Repository URL: https://github.com/nishan1314/acts-ict.git
echo.
pause
