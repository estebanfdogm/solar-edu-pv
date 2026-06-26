# Ejecutable de SolarEdu PV para Windows

## Crear el ejecutable

1. Abra una terminal en la carpeta del proyecto.
2. Ejecute:

   ```bat
   build_exe.bat
   ```

   El script instala las dependencias de `requirements.txt`, limpia compilaciones anteriores y genera una distribución de PyInstaller en modo `--onedir`.

## Ubicación del resultado

Al finalizar, el ejecutable queda en:

```text
dist\SolarEduPV\SolarEduPV.exe
```

Conserve toda la carpeta `dist\SolarEduPV\`; el `.exe` necesita los archivos que la acompañan.

## Uso

1. Haga doble clic en `SolarEduPV.exe`.
2. El lanzador inicia el servidor local en el puerto `8501`.
3. El navegador se abre automáticamente en `http://localhost:8501`.
4. Mantenga abierta la ventana de consola mientras utiliza la aplicación.

Para cerrar SolarEdu PV, cierre la ventana de consola del lanzador. También puede cerrar la pestaña del navegador cuando ya no vaya a usarla.

## Advertencia de Windows Defender

Un ejecutable creado localmente y sin firma digital puede mostrar una advertencia de SmartScreen o Windows Defender. Si el archivo fue generado por usted con `build_exe.bat` desde este proyecto, revise la ruta y seleccione **Más información** → **Ejecutar de todas formas**. No ejecute archivos procedentes de fuentes no confiables.

## Prueba en modo desarrollo

Antes de compilar, puede comprobar el lanzador con:

```powershell
python launcher.py
```

El comportamiento es equivalente a ejecutar `streamlit run app.py --server.port 8501 --server.headless true`, con apertura automática del navegador.
