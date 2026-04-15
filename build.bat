@echo off
echo ============================================
echo  GI-FORCE - Gerando Executavel
echo ============================================
echo.

REM Instala dependencias
echo [1/4] Instalando dependencias...
python -m pip install pygame pyinstaller

echo.
echo [2/4] Compilando com PyInstaller...
python -m PyInstaller --onefile --windowed --name "GiForce" --icon "assets\images\spaceship.ico" main.py

echo.
echo [3/4] Copiando assets para a pasta de distribuicao...
if not exist assets goto :sem_assets

echo import os, shutil > _copy_assets.py
echo src = 'assets' >> _copy_assets.py
echo dst = os.path.join('dist', 'assets') >> _copy_assets.py
echo copied = 0 >> _copy_assets.py
echo skipped = 0 >> _copy_assets.py
echo for root, dirs, files in os.walk(src): >> _copy_assets.py
echo     for f in files: >> _copy_assets.py
echo         s = os.path.join(root, f) >> _copy_assets.py
echo         d = os.path.join(dst, os.path.relpath(s, src)) >> _copy_assets.py
echo         os.makedirs(os.path.dirname(d), exist_ok=True) >> _copy_assets.py
echo         if not os.path.exists(d) or os.path.getsize(s) != os.path.getsize(d): >> _copy_assets.py
echo             shutil.copy2(s, d) >> _copy_assets.py
echo             copied += 1 >> _copy_assets.py
echo         else: >> _copy_assets.py
echo             skipped += 1 >> _copy_assets.py
echo print('Assets: ' + str(copied) + ' copiado(s), ' + str(skipped) + ' ignorado(s).') >> _copy_assets.py

python _copy_assets.py
del _copy_assets.py
goto :fim_assets

:sem_assets
echo Pasta assets nao encontrada, pulando copia...

:fim_assets
echo.
echo ============================================
echo  PRONTO! Executavel em: dist\GiForce.exe
echo.
echo  Para distribuir, compacte a pasta "dist"
echo  em um arquivo ZIP e envie como entrega.
echo ============================================
pause
