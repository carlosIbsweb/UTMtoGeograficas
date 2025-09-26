@echo off
echo Instalando dependencias para Conversao UTM...
echo.

REM Verifica se Python esta instalado
py --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado! Por favor, instale o Python primeiro.
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado! Instalando dependencias...
echo.

REM Instala as dependencias
py -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo Instalacao concluida com sucesso!
echo.
echo Para executar o programa, use: py conversao_utm.py
echo.
pause
