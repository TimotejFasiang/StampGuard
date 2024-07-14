# Updates for doc. Chaloupka:

### 3:
Brzy budu přidávat "releases" na svou stránku na githubu, ale zatím, pokud se chcete podívat, můžete si naklonovat můj repozitář a pak z hlavního adresáře (v Linuxu) otevřít terminál a spustit "npm run tauri dev".
Potrebujete jenom [rust](https://www.rust-lang.org/tools/install) a [Node.js](https://nodejs.org/en)

### 2:
Pro aplikaci jsem se rozhodl použít Tauri. Je to moderní framework pro vytváření multiplatformních desktopových aplikací využívajících webové technologie (v mém případě HTML, CSS a JavaScript) v kombinaci s Rustem pro backendové funkce. I když jako backend používá rust, budu ho používat pouze k volání svých python souborů, takže teoreticky by se dalo říct, že má pythonovský backend, jak jste požadoval.
Základy jsem dokončil. Mám úvodní stránku s výběrem jazyka(en/cz) a pak hlavní stránku, kde si uživatel může vybrat obrázek ze svého počítače, a můj javascriptový kód vyvolá příkaz rustu, který spustí můj pythonový soubor a uloží upravený obrázek(zatím jen vodorovné překlopení, aby bylo jisté, že python lze použít), který se pak zobrazí v aplikaci.

### 1:
Měl jsem schůzku s Ing. Chudobou a diskutovali jsme o tom, co by chtěl, aby aplikace dělala. Mám několik verzí známek z roku 1919, se kterými mi doporučil začít. Například na jedné z verzí je klíčovým ukazatelem toho, zda je známka pravá nebo falešná, háček na s. Na předchozím obrázku se háček téměř dotýká s, kdežto na dalším obrázku je háček vyvýšen nad s. Podobné typy ukazatelů jsou i na dalších známkách. Zmínil také, že vzhledem k tomu, že známky jsou více než 100 let staré, nemusí mít již stejné rozměry a mezi pravou a falešnou může být rozdíl jen několika milimetrů.

## - - - - - - - - - - - - - - - - - - - -

# StampGuard

StampGuard is a cross-platform desktop (mobile maybe ??) application designed to detect fraud and fake Czechoslovak stamps. It utilizes algorithms to analyze and verify the authenticity of stamps based on various criteria.

## Features

- **Stamp Image Analysis:** Upload a photo of a stamp to analyze its authenticity.
- **Advanced Algorithms:** Utilizes advanced models and image processing algorithms to detect patterns indicative of fraudulent or fake stamps.
- **User-friendly Interface:** Simple and intuitive UI for easy operation and analysis.
- **Offline Mode:** Works entirely offline, no need for internet connectivity for stamp verification.
- **Detailed Findings:** Provides detailed findings on the analysis and authenticity of each stamp.
- **Customizable Settings:** Adjustable settings for different stamp types and verification thresholds.
- **Other:** Other features.

## Getting Started

### Prerequisites

- Windows, macOS, or Linux operating system
- Maybe Android or IOS phone??
- Other prerequisites

### Installation

1. **Visit the Releases Page**:
   Go to the [Releases page](https://github.com/TimotejFasiang/StampGuard/releases/).

2. **Download the Latest Release**:
   Find the latest release and download the appropriate file for your operating system:
   - For Windows: `StampGuard-x.x.x-win64.zip`
   - For macOS: `StampGuard-x.x.x-mac.zip`
   - For Linux: `StampGuard-x.x.x-linux.tar.gz`

3. **Extract the Archive**:
   Extract the downloaded archive to a desired location on your computer.

4. **Run the Software**:
   Navigate to the extracted folder and run the executable file:
   - On Windows: Double-click `StampGuard.exe`
   - On macOS: Open `StampGuard.app`
   - On Linux: Run `./StampGuard.sh` from the terminal
