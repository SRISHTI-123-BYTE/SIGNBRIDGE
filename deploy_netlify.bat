@echo off
echo =========================================================================
echo  SignBridge: Netlify Deployment Helper
echo =========================================================================
echo.
echo Your repository is ready with netlify.toml and _redirects configured:
echo GitHub: https://github.com/SRISHTI-123-BYTE/SIGNBRIDGE
echo.
echo Opening Netlify Drop in your browser...
start https://app.netlify.com/drop
echo Opening frontend\dist folder in Windows Explorer...
start explorer.exe "%~dp0frontend\dist"
echo.
echo [INSTRUCTIONS]
echo Simply drag the contents of the opened 'dist' folder into the Netlify Drop browser box.
echo Netlify will publish your site in 5 seconds and give you a live URL!
echo.
pause
