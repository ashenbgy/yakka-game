# Yaksha Kombat — යක්ෂ සටන 👹⚔️

> **A zero-install, 3D browser fighting game inspired by Sri Lankan yakku folklore, demonology, and Thovil rituals.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Three.js](https://img.shields.io/badge/Three.js-r160-black.svg?logo=three.js)](https://threejs.org/)
[![WebGL](https://img.shields.io/badge/WebGL-2.0-990000.svg?logo=webgl)](https://www.khronos.org/webgl/)
[![WebRTC](https://img.shields.io/badge/WebRTC-PeerJS-333333.svg?logo=webrtc)](https://peerjs.com/)
[![Web Audio API](https://img.shields.io/badge/Web_Audio-Procedural_Synthesis-blue.svg)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

---

## 🎮 Overview

**Yaksha Kombat (යක්ෂ සටන)** brings traditional Sri Lankan mythic lore, demonology (*yakku*), and ancient *Thovil* (exorcism ritual) aesthetic into an arcade-style 2.5D fighting game. 

Built entirely with standard web standards, the game requires **zero downloads, zero installations, and zero build steps**—running directly in any modern desktop or mobile browser.

---

## ✨ Key Features

- 👹 **18 Mythical Fighters:** Play as folklore demons and archetypes including *Gal Yaka*, *Le Yaka*, *Kadu Kumaraya*, *Mala Hewaya*, *Sohon Yaka*, *Gami Kumari*, *Asura Rajaya*, *Kabara Yakini*, and more.
- 🏛️ **7 Sri Lankan Stages:** Battle across atmospheric 3D arenas including Sigiriya, Ella Tea Estates, Paddy Fields, Southern Beach, Deep Jungle, Traditional Village, and Asura Palace.
- 🥊 **Frame-Data Combat Physics:** Custom fighting engine featuring active hitboxes, hitstop freeze-frames, hitstun, pushback physics, wall bounces, corner pushback, dodges, and multi-hit combos.
- 🌐 **P2P Multiplayer via WebRTC:** Direct peer-to-peer online play with 4-digit room codes powered by WebRTC data channels (no external game servers required).
- 🥁 **Procedural Sri Lankan Ritual Audio:** Real-time synthesis of traditional percussion instruments (*Yak Bera* drum sounds: *Thom*, *Tha*, *Thei*, *Kadittu*, *Mandra*), *Thalam* cymbals, and the microtonal *Horanewa* double-reed horn using the Web Audio API.
- 🩸 **Ritual Finishers (*Bili* / Fatalities):** Win the final round to execute traditional ritual sacrifices: *Bili* (බිලි), *Maha Bili* (මහා බිලි), or *Shanthiya* (ශාන්තිය - mercy).
- 📱 **Mobile & Touch Support:** Automatic virtual touch D-pad and responsive action buttons for touchscreen devices.
- 🇱🇰 **Bespoke Sinhala Typography:** UI rendered with authentic Sinhala typefaces (*Gemunu Libre* & *Yaldevi* by Mooniak foundry).

---

## 🕹️ Controls

### Keyboard Controls

| Action | Primary Key | Secondary Key |
| :--- | :--- | :--- |
| **Move Left / Right** | <kbd>A</kbd> / <kbd>D</kbd> | <kbd>←</kbd> / <kbd>→</kbd> |
| **Jump** | <kbd>W</kbd> | <kbd>↑</kbd> |
| **Crouch (Hold)** | <kbd>S</kbd> | <kbd>↓</kbd> |
| **Roll / Dodge** | <kbd>Shift</kbd> + <kbd>←</kbd> / <kbd>→</kbd> | <kbd>Shift</kbd> (neutral) |
| **Block (Hold)** | <kbd>Space</kbd> | — |
| **Lead Punch (High)** | <kbd>J</kbd> | — |
| **Rear Punch (Power)** | <kbd>I</kbd> | — |
| **Lead Kick (Mid)** | <kbd>K</kbd> | — |
| **Rear Kick (Heavy)** | <kbd>L</kbd> | — |
| **Slide Attack (Low)** | <kbd>↓</kbd> + <kbd>K</kbd> / <kbd>L</kbd> | — |
| **Jump Kick (Air)** | <kbd>→</kbd> + <kbd>L</kbd> | — |
| **Thovil Super Attack** | <kbd>O</kbd> *(when gauge is full)* | — |
| **Pause / Menu** | <kbd>Esc</kbd> | — |
| **Mute / Unmute Audio** | <kbd>M</kbd> | — |

> **Special Moves:** Directional sequence followed by attack button (e.g. <kbd>↓</kbd> <kbd>→</kbd> <kbd>J</kbd>). Direction arrows are relative to opponent orientation (<kbd>→</kbd> is toward opponent).  
> **Post-Round Finishers:** When prompted, press <kbd>J</kbd> for *Bili*, <kbd>I</kbd> for *Maha Bili*, or <kbd>K</kbd> for *Shanthiya*.

### Touch Controls
On mobile or touchscreen devices, an on-screen D-pad and dedicated attack buttons appear automatically.

---

## 🛠️ Architecture & Tech Stack

```
yakka-game/
├── index.html                 # Complete single-page game engine & UI
├── favicon.png                # App icon
├── assets/
│   ├── arenas/                # High-res stage backdrops (Sigiriya, Ella, etc.)
│   ├── music/                 # Menu theme ("Drums in the Deepwood")
│   └── *.jpg, *.hdr           # PBR environment textures and HDR skyboxes
└── models/
    ├── characters/            # 18 distinct GLTF/GLB character models
    └── anims/                 # Mixamo FBX motion capture clips (50+ clips)
```

- **Renderer:** [Three.js](https://threejs.org/) (r160) utilizing WebGL 2.0 with `EffectComposer`, `UnrealBloomPass`, and custom shader passes.
- **Animation Pipeline:** Mixamo mocap retargeted at runtime across distinct skeletal rigs using Three.js `SkeletonUtils`.
- **Procedural Sound Engine:** Web Audio API graph utilizing custom oscillator arrays, bi-quad bandpass/lowpass filters, noise buffers, and convolver reverbs for traditional Sri Lankan percussion and horns.
- **Netcode:** [PeerJS](https://peerjs.com/) WebRTC data channels for low-latency peer-to-peer state synchronization via 4-digit numeric room codes.
- **Zero-Build:** Standard ES modules via browser `<script type="importmap">`, eliminating bundling or compilation steps.

---

## 🚀 Running Locally

Because the game loads 3D models (`.glb`, `.fbx`) and textures via `fetch()`, it requires a local web server to avoid browser CORS restrictions.

### Option 1: Python (Built-in)
```bash
# Python 3
python3 -m http.server 8000
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

### Option 2: Node.js (npx serve)
```bash
npx serve .
```

### Option 3: VS Code Live Server
Right-click `index.html` inside VS Code and choose **"Open with Live Server"**.

---

## 👥 Roster Preview

| Fighter | Sinhala | Archetype |
| :--- | :--- | :--- |
| **Gal Yaka** | ගල් යකා | Heavy Brawler / Earth Slammer |
| **Le Yaka** | ලේ යකා | Bloodthirsty Rushdown Striker |
| **Kadu Kumaraya** | කඩු කුමාරයා | Agile Swordsman & Teleporter |
| **Mala Hewaya** | මල හේවයා | Plague Commander & Debuffer |
| **Hora Yaka** | හොර යකා | Deceptive Counter Fighter |
| **Pachcha Yaka** | පච්ච යකා | Hex & Puppet Caster |
| **Wattakka Yaka** | වට්ටක්කා යකා | High Defense Mountain Guardian |
| **Gami Kumari** | ගැමි කුමාරි | Trap Weaver & Siren |
| **Badagini Yaka** | බඩගිනි යකා | Ravenous Life-Drain Grappler |
| **Asura Rajaya** | අසුර රාජයා | Boss Emperor / Area-of-Effect Titan |
| **Nil Yaka** | නිල් යකා | Flame Demon & Projectile Specialist |
| **Ang Yaka** | අං යකා | Horned Poison Wrestler |
| **Kola Yaka** | කොළ යකා | Aerial Striker & Gale Force |
| **Sohon Yaka** | සොහොන් යකා | Graveyard Executioner |
| **Kabara Yakini** | කබර යකිණි | Swift Reptilian Assassin |
| **Mayakari Yakini** | මායාකාරී යකිණි | Dark Sorceress / Illusionist |
| **Sema Demon** | සෙමා ඩීමන් | Shadow Warrior |
| **Biped Robot** | යකඩ යන්ත්‍රය | Cyber Mech / Laser Striker |

---

## 📜 Credits & Attributions

- **Game Design & Development:** [Ashenbgy](https://github.com/ashenbgy)
- **3D Character Rigs & Combat Animations:** [Mixamo (Adobe)](https://www.mixamo.com/)
- **Additional 3D Models:**
  - *Sema Demon* by krit yamsaso ([CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/))
  - *Biped Robot* by Willy Decarpentrie ([CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/))
  - Base humanoid meshes from Three.js examples
- **Environment Maps & Textures:** [Poly Haven](https://polyhaven.com/) (CC0)
- **Menu Music:** *"Drums in the Deepwood"* by Elyvilon ([CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/))
- **Typography:** *Gemunu Libre* & *Yaldevi* by [Mooniak](https://mooniak.com/) (SIL Open Font License)

---

## ⚖️ License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

