@echo off
SETLOCAL

echo input
set /p "file=Enter a path to a .wav file (it cannot have spaces): "
FOR /F "delims=" %%i IN ("%file%") DO (
    set "filedrive=%%~di"
    set "filepath=%%~pi"
    set "filename=%%~ni"
    set "fileextension=%%~xi"
)

echo settings
set /a t=127
set /a b=0
set /p "s=Shift: "
set /p "nfft=NFFT (if you don't know what this is then just type 2048): "
set /p "peak=Peak (if you want chunks then type -127 and make sure shift isn't below 768, and if you don't, just type 127 and there isn't a shift limit on this one): "
set /p "www=Window (0-no window 1-parzen window 2-welch window 3-hanning window (recommended) 4-hamming window 5-blackman window 6-steeper 30-dB/octave rollof window) so choose a window: "
set /p "trak=uhh tracks (16 or 32 recommended): "

echo "duplicate input with no spaces as said converter will not work if the input name has spaces in it."
copy /y "%file%" "C:\Users\%USERNAME%\audio.wav"

set "output=%filename%_t-%t%_b-%b%_s-%s%_p-%peak%_window-%www%_c_-7.mid"

echo "main command(waon)"
start "" /B "C:\Users\%USERNAME%\Downloads\waon0-9\waon.exe" -t %t% -b %b% -s %s% -c -6.414 -k %peak% -w %www% -i "C:\Users\%USERNAME%\audio.wav" -o "%output%"

:WAON_WAIT
timeout /t 1 /nobreak >nul
tasklist /FI "IMAGENAME eq waon.exe" | find /i "waon.exe" >nul
if errorlevel 1 (
    echo "waon.exe has finished processing."
) else (
    goto WAON_WAIT
)

echo "adding tracks (you selected amount)"
start "" /B "C:\Users\%USERNAME%\Downloads\velocity\velocity.exe" "%output%" "%filename%_t-%t%_b-%b%_s-%s%_p-%peak%_window-%www%-colored.mid" %trak%

:PY39_WAIT
timeout /t 1 /nobreak >nul
tasklist /FI "IMAGENAME eq velocity.exe" | find /i "velocity.exe" >nul
if errorlevel 1 (
    echo "velocity.exe has finished processing."
) else (
    goto PY39_WAIT
)

echo "deleting temporary files"
del "%output%"
del "C:\Users\%USERNAME%\audio.wav"
