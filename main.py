import time
import random
import os
import shutil

p = {
    "electron": {"m": 0.5, "c": -1, "n": "electron"},
    "positron": {"m": 0.5, "c": 1, "n": "positron"},
    "proton": {"m": 938, "c": 1, "n": "proton"},
    "neutron": {"m": 940, "c": 0, "n": "neutron"},
    "photon": {"m": 0, "c": 0, "n": "photon"},
    "muon": {"m": 106, "c": -1, "n": "muon"},
    "pion": {"m": 140, "c": 0, "n": "pion"},
    "neutrino": {"m": 0.001, "c": 0, "n": "neutrino"},
    "kaon": {"m": 494, "c": 0, "n": "kaon"},
    "antiproton": {"m": 938, "c": -1, "n": "antiproton"}
}

last = None

def show():
    print("\n Select what you want to collide:")
    for n, d in p.items():
        print(f"- {n}: mass = {d['m']} MeV, charge = {d['c']}")

def pick():
    pl = list(p.keys())
    print("\nAvailable particles:")
    for i, n in enumerate(pl, 1):
        d = p[n]
        print(f"{i}. {n} (mass: {d['m']} MeV, charge: {d['c']})")
    
    while True:
        c = input("\nPick a particle (name or number): ").strip()
        
        try:
            num = int(c)
            if 1 <= num <= len(pl):
                n = pl[num - 1]
                return n, p[n]
            else:
                print(f"Pick a number between 1 and {len(pl)}!")
                continue
        except ValueError:
            pass
        
        n = c.lower()
        if n in p:
            return n, p[n]
        
        print("Hmm, I don't know that one. Try again!")

def get_e():
    print("\nEnergy guide (all in MeV):")
    print("- Low energy (1-10): Like a gentle push")
    print("- Medium energy (50-200): Like a baseball throw") 
    print("- High energy (500-1000): Like a rocket launch")
    print("- Super high (1000+): Like lightning!")
    print("\nFor comparison:")
    print("- Chemical reactions: ~1-10 MeV")
    print("- Nuclear reactions: ~100-1000 MeV")
    print("- Particle accelerators: 1000+ MeV")
    print("- dont event think about 5000+ thats like a supernova!!!!!")
    
    while True:
        try:
            e = float(input("\nHow much energy does it have? (in MeV) "))
            if e > 0:
                return e
            print("Energy has to be more than zero lol!")
        except ValueError:
            print("That's not a number !!!! Try again bro")

def chk(p1, p2, res):
    sc = p1["c"] + p2["c"]
    ec = sum(p[part]["c"] for part in res)
    return sc == ec

def calc(p1, p1d, e1, p2, p2d, e2):
    global last
    te = e1 + e2
    
    last = {
        "p1": p1, "p1d": p1d, "e1": e1,
        "p2": p2, "p2d": p2d, "e2": e2,
        "te": te
    }
    
    if (p1 == "electron" and p2 == "positron") or (p1 == "positron" and p2 == "electron"):
        if te > 1:
            return ["photon", "photon"], "Boom! They destroyed each other and made light!"
    
    # photon
    if p1 == "photon" or p2 == "photon":
        if te > 200:
            return ["electron", "positron"], "The light made new particles!"
        else:
            return [p1, p2], "The light just bounced off"
    
    # high energy
    if te > 1000:
        if p1d["c"] != 0 and p2d["c"] != 0:
            return ["proton", "neutron", "pion"], "Huge crash! Made lots of new stuff!"
    
    # medium energy
    if te > 500:
        return ["muon", "pion"], "Made some medium heavy particles!"
    
    # small crashes
    if te > 50:
        return [p1, p2], "They bounced off each other like rubber balls!"
    
    # gentle
    return [p1, p2], "They barely touched and kept going haha throw them harder!!!"

def crash():
    print("\n=== Time for a particle crash! ===")
    
    print("\nFirst particle:")
    p1n, p1d = pick()
    e1 = get_e()
    
    print("\nSecond particle:")
    p2n, p2d = pick()
    e2 = get_e()
    
    te = e1 + e2
    print("\n COLLISION SETUP:")
    print(f"   {p1n} with {e1} MeV + {p2n} with {e2} MeV")
    print(f"   Total energy: {te} MeV")
    print(f"   Energy level: {get_el(te)}")
    
    res, story = calc(p1n, p1d, e1, p2n, p2d, e2)
    
    anim(p1n, p2n, res, story)
    
    print(f"\n What happened: {story}")
    print(" After the crash, we found:")
    for part in res:
        if part in p:
            d = p[part]
            print(f"   - {part} (mass: {d['m']} MeV, charge: {d['c']})")
    
    if chk(p1d, p2d, res):
        print("Charge conservation: All good!")
    else:
        print("Charge conservation: Something weird happened...")
    
    show_sum(p1n, p2n, res, story)

def get_el(e):
    if e < 10:
        return "Very gentle (thermal motion)"
    elif e < 100:
        return "Moderate (chemical reaction level)"
    elif e < 500:
        return "High (nuclear reaction level)"
    elif e < 1000:
        return " Very high (particle accelerator)"
    elif e < 2000:
        return " Extreme (Large Hadron Collider)"
    else:
        return "COSMIC! (like in space!)"

def look():
    print("\n=== Particle Detective Mode ===")
    name, data = pick()
    
    print(f"\n Examining {name} under our super microscope...")
    print(f"Mass: {data['m']} MeV (that's how heavy it is)")
    print(f" Charge: {data['c']} (positive, negative, or neutral)")
    
    facts = {
        "electron": "This little guy makes electricity work! It's so small it might be point-like!",
        "positron": "This is like an electron but backwards! When it meets an electron: BOOM!",
        "proton": "This lives in the middle of atoms. It's made of 3 smaller things called quarks!",
        "neutron": "This also lives in atoms but has no charge. It can turn into a proton!",
        "photon": "This is pure light! It has no weight at all and always moves at light speed!",
        "muon": "This is like a heavy electron that doesn't last long. It lives for 2 microseconds!",
        "pion": "This helps hold the atom's center together. It's a 'meson' made of quarks!",
        "neutrino": "This is a ghost particle! Trillions pass through you every second!",
        "kaon": "This is a strange particle (literally has 'strangeness'). Very exotic!",
        "antiproton": "This is the evil twin of a proton! Made in particle accelerators!"
    }
    
    if name in facts:
        print(f"Cool fact: {facts[name]}")
    
    locations = {
        "electron": " Found in: Every atom, electrical wires, your computer screen!",
        "positron": " Found in: PET scans, cosmic rays, some radioactive decay!",
        "proton": "Found in: Every atom's nucleus, cosmic rays, the sun!",
        "neutron": " Found in: Atomic nuclei, nuclear reactors, neutron stars!",
        "photon": " Found in: Light, radio waves, X-rays, your WiFi signal!",
        "muon": "Found in: Cosmic rays, particle accelerators, upper atmosphere!",
        "pion": " Found in: Cosmic ray showers, particle collisions!",
        "neutrino": " Found in: The sun, nuclear reactors, everywhere (but invisible)!",
        "kaon": " Found in: High energy cosmic rays, particle accelerators!",
        "antiproton": " Found in: CERN, cosmic ray interactions, antimatter research!"
    }
    
    if name in locations:
        print(locations[name])

def replay():
    if lastcoll is None:
        print("\n No collision to replay! Do a collision first.")
        return
    
    print("\n REPLAYING LAST COLLISION...")
    print("=" * 50)
    
    p1 = lastcoll["p1"]
    p2 = lastcoll["p2"]
    e1 = lastcoll["e1"] 
    e2 = lastcoll["e2"]
    total_e = lastcoll["te"]
    
    print(f" Repeating: {p1} ({e1} MeV) + {p2} ({e2} MeV)")
    print(f"   Total energy: {total_e} MeV")
    
    input("\nPress Enter to replay the collision...")
    
    p1_data = p[p1]
    p2_data = p[p2]
    res, story = calc(p1, p1_data, e1, p2, p2_data, e2)
    
    anim(p1, p2, res, story)
    
    print(f"\n REPLAY RESULT: {story}")
    print("You might get some different result due to quantum stuff that neither of us know about lol")




def clr():
    os.system("cls" if os.name == "nt" else "clear")

def anim(p1, p2, res, story):
    syms = {
        "electron": "e-", "positron": "e+", "proton": "p+",
        "neutron": "n0", "photon": "Y", "muon": "u-", "pion": "pi",
        "neutrino": "v", "kaon": "K0", "antiproton": "p-"
    }

    s1 = syms.get(p1, "?")
    s2 = syms.get(p2, "?")

    print(f"\nStarting this beast!!!! {s1} + {s2}")
    print("Beam alignment in progress...")
    time.sleep(1.5)

    cw = min(shutil.get_terminal_size((120, 20)).columns, 120)
    innerw = cw - 2
    collrow = 18 // 2

    def drawchamb(partdata=None, trails=None):
        lines = []
        lines.append("+" + "=" * innerw + "+")
        for row in range(18):
            if row == 0:
                lines.append("|" + "CERN Large Hadron Collider - Particle Detector".center(innerw) + "|")
            elif row == 1:
                lines.append("|" + " " * innerw + "|")
            elif row == 2 or row == (15):
                lines.append("|" + "." * innerw + "|")
            else:
                line_content = [" "] * innerw
                if trails and row in trails:
                    for pos in trails[row]:
                        if 0 <= pos < innerw:
                            line_content[pos] = "."
                if partdata and row in partdata:
                    for pos, symbol in partdata[row]:
                        if 0 <= pos < innerw:
                            for i, ch in enumerate(symbol):
                                if 0 <= pos+i < innerw:
                                    line_content[pos+i] = ch
                lines.append("|" + "".join(line_content) + "|")
        lines.append("+" + "=" * innerw + "+")
        return "\n".join(lines)

    clr()
    print(drawchamb())
    time.sleep(1.2)

    center = innerw // 2

    print("\nParticle beams approaching collision point...")
    time.sleep(0.8)

    for step in range(20):
        left_pos = step * 3
        right_pos = innerw - 1 - (step * 3)
        if left_pos >= right_pos - 3:
            break

        partdata = {
            collrow: [(left_pos, s1), (right_pos, s2)]
        }

        btrails = {}
        if left_pos > 5:
            btrails.setdefault(collrow, []).append(left_pos - 3)
        if right_pos < innerw - 5:
            btrails.setdefault(collrow, []).append(right_pos + 3)

        if step % 2 == 0:
            clr()
            print(f"Beam energy: {step * 5}% of maximum | Collision imminent")
            print(drawchamb(partdata, btrails))
        time.sleep(0.3)

    clr()
    print("COLLISION EVENT DETECTED!!!!!!")
    print(drawchamb({
        collrow: [(center-1, s1), (center, "*"), (center+1, s2)]
    }))
    time.sleep(1.2)

    clr()
    print("High energy interaction detected!!!")
    print(drawchamb({
        collrow: [(center, "+")]
    }))
    time.sleep(0.8)

    ressymb = [syms.get(p, "?") for p in res]
    traject = []
    ptrails = {}

    if "destroyed" in story.lower() or "annihilated" in story.lower():
        for i, symbol in enumerate(ressymb[:2]):
            direction = 1 if i == 0 else -1
            traject.append({
                'symbol': symbol,
                'start_x': center,
                'start_row': collrow,
                'dx': direction * 4,
                'dy': 0,
                'steps': 22,
                'trail_length': 8
            })
    elif "bounced" in story.lower():
        for i, symbol in enumerate(ressymb[:2]):
            direction = 1 if i == 0 else -1
            angle = random.uniform(15, 45) if i == 0 else random.uniform(-45, -15)
            angle_rad = angle * 3.14159 / 180
            speed = 3.5
            traject.append({
                'symbol': symbol,
                'start_x': center,
                'start_row': collrow,
                'dx': direction * speed * abs(angle_rad * 2),
                'dy': speed * angle_rad * 0.8,
                'steps': 18,
                'trail_length': 6
            })
    elif "made" in story.lower() or "new" in story.lower():
        angles = [0, 30, -30, 60, -60, 90, -90, 120, -120]
        for i, symbol in enumerate(ressymb):
            if i < 6:
                angle = angles[i % len(angles)] + random.uniform(-10, 10)
                angle_rad = angle * 3.14159 / 180
                speed = 3.2 + random.uniform(-0.5, 0.5)
                traject.append({
                    'symbol': symbol,
                    'start_x': center,
                    'start_row': collrow,
                    'dx': speed * (1 if angle_rad > 0 else -1) * (1 + abs(angle_rad) * 0.5),
                    'dy': speed * angle_rad * 0.6,
                    'steps': 16 + random.randint(0, 6),
                    'trail_length': 5
                })
    else:
        for i, symbol in enumerate(ressymb[:2]):
            direction = 1 if i == 0 else -1
            angle_rad = random.uniform(-20, 20) * 3.14159 / 180
            traject.append({
                'symbol': symbol,
                'start_x': center,
                'start_row': collrow,
                'dx': direction * 2.5,
                'dy': angle_rad * 2,
                'steps': 14,
                'trail_length': 4
            })

    for i in range(len(traject)):
        ptrails[i] = []

    max_steps = max(t['steps'] for t in traject)

    for step in range(max_steps):
        partdata = {}
        current_trails = {}

        for i, traj in enumerate(traject):
            if step < traj['steps']:
                x = int(traj['start_x'] + traj['dx'] * step * 0.7)
                y = traj['start_row'] + traj['dy'] * step * 0.12

                if abs(traj['dy']) > 0.5:
                    y += 0.3 * (step / traj['steps']) ** 2 * (1 if traj['dy'] > 0 else -1)

                row = int(y)

                if 3 <= row < 18 - 3 and 0 <= x < innerw:
                    partdata.setdefault(row, []).append((x, traj['symbol']))
                    ptrails[i].append((x, row))
                    if len(ptrails[i]) > traj['trail_length']:
                        ptrails[i].pop(0)

        for i, trail in ptrails.items():
            for x, row in trail[:-1]:
                if 3 <= row < 18 - 3 and 0 <= x < innerw:
                    current_trails.setdefault(row, []).append(x)

        clr()
        print(f"Tracking {len(res)} particles | Frame {step+1}/{max_steps}")
        print("Multi-layer calorimeter: Recording energy deposits")
        print(drawchamb(partdata, current_trails))
        time.sleep(0.15)

    clr()
    print("Event reconstruction complete | Physics analysis successful")
    print(f"Collision outcome: {story}")
    print(f"Detected particles: {' + '.join(res)}")

    final_particles = {}
    final_trails = {}

    for trail in ptrails.values():
        for x, row in trail:
            if 3 <= row < 18 - 3 and 0 <= x < innerw:
                final_trails.setdefault(row, []).append(x)

    for i, symbol in enumerate(ressymb[:6]):
        if i < 3:
            x = max(8, center - 35 + i * 6)
            row = collrow + (i - 1) * 3 + random.randint(-2, 2)
        else:
            x = min(innerw - 8, center + 35 - (i-3) * 6)
            row = collrow + ((i-3) - 1) * 3 + random.randint(-1, 1)

        if 3 <= row < 18 - 3:
            final_particles.setdefault(row, []).append((x, symbol))

    print(drawchamb(final_particles, final_trails))
    print("\nParticle identification complete. Trajectories reconstructed.")
    print("Event logged to physics database. Ready for next collision.")


def random_collision():
    print("\n=== RANDOM COLLISION EXPERIMENT ===")
    print("Let the quantum universe decide what crashes together!")
    
    pname = list(p.keys())
    p1n = random.choice(pname)
    p2n = random.choice(pname)
    
    energy_ranges = [
        (1, 50, "Low energy (thermal/chemical)"),
        (50, 500, "Medium energy (nuclear)"), 
        (500, 2000, "High energy (particle accelerator)"),
        (2000, 10000, "Ultra-high energy (cosmic ray)")
    ]
    
    range1 = random.choice(energy_ranges)
    range2 = random.choice(energy_ranges)
    
    e1 = random.uniform(range1[0], range1[1])
    e2 = random.uniform(range2[0], range2[1])
    
    print(f"\nRandom selection:")
    print(f"   Particle 1: {p1n} @ {e1:.1f} MeV ({range1[2]})")
    print(f"   Particle 2: {p2n} @ {e2:.1f} MeV ({range2[2]})")
    print(f"   Total energy: {e1 + e2:.1f} MeV")
    
    input("\nPress Enter to run the random collision...")
    
    global lastcoll
    lastcoll = {
        "p1": p1n, "p1d": p[p1n], "e1": e1,
        "p2": p2n, "p2d": p[p2n], "e2": e2,
        "te": e1 + e2
    }
    
    res, story = calc(p1n, p[p1n], e1, p2n, p[p2n], e2)
    
    anim(p1n, p2n, res, story)
    
    print(f"\nRandom collision result: {story}")
    print("Final particles detected:")
    for particle in res:
        if particle in p:
            data = p[particle]
            print(f"   - {particle} (mass: {data['m']} MeV, charge: {data['c']})")
    
    p1_data = p[p1n]
    p2_data = p[p2n]
    if chk(p1_data, p2_data, res):
        print("Charge conservation: Verified!")
    else:
        print("Charge conservation: Anomaly detected!")
    
    choice = input("\nWant detailed physics analysis? (y/n): ").strip().lower()
    if choice == 'y' or choice == 'yes':
        show_sum(p1n, p2n, res, story)



def show_sum(p1, p2, res, story):    
    print("\n" + "="*90)
    print(" PARTICLE PHYSICS COLLISION ANALYSIS REPORT".center(90))
    print("="*90)
    
    cd = last
    p1d = p[p1]
    p2d = p[p2]
    te = cd['te']
    
    import math
    p1m = p1d['m']
    p2m = p2d['m']
    e1 = cd['e1']
    e2 = cd['e2']
    
    s = (p1m + p2m + te/2)**2
    sqrt_s = math.sqrt(s)
    
    print(f"\nCOLLISION KINEMATICS:")
    print(f"   Beam A: {p1} @ {e1:.1f} MeV (rest mass: {p1m} MeV/c^2)")
    print(f"   Beam B: {p2} @ {e2:.1f} MeV (rest mass: {p2m} MeV/c^2)")
    print(f"   Total Lab Energy: {te:.1f} MeV")
    print(f"   Center-of-Mass Energy (sqrt(s)): {sqrt_s:.1f} MeV")
    
    totmass = p1m + p2m
    totout = sum(p[part]['m'] for part in res if part in p)
    fmass = totmass - totout
    
    print(f"\nREACTION ENERGETICS:")
    print(f"   Initial rest mass: {totmass:.1f} MeV/c^2")
    print(f"   Final rest mass: {totout:.1f} MeV/c^2")
    print(f"   Q-value: {fmass:.1f} MeV {'(exothermic)' if fmass > 0 else '(endothermic)'}")
    print(f"   Available kinetic energy: {te + fmass:.1f} MeV")
    
    # Conservation laws check
    totc = p1d['c'] + p2d['c']
    totoutc = sum(p[part]['c'] for part in res if part in p)
    
    print(f"\nCONSERVATION LAWS:")
    charge_conserved = (totc == totoutc)
    print(f"   Electric charge: {totc} -> {totoutc} {'CONSERVED' if charge_conserved else 'VIOLATED'}")
    
    # Energy momentum conservation
    energy_conserved = te >= (totmass - totout)
    print(f"   Energy-momentum: {'CONSERVED' if energy_conserved else 'CHECK REQUIRED'}")
    
    # Baryon number conservation (simplified)
    baryon_input = sum(1 for p in [p1, p2] if p in ['proton', 'neutron', 'antiproton'])
    baryon_output = sum(1 for p in res if p in ['proton', 'neutron', 'antiproton'])
    if baryon_input > 0 or baryon_output > 0:
        print(f"   Baryon number: {baryon_input} -> {baryon_output} {'CONSERVED' if baryon_input == baryon_output else 'CHECK'}")
    
    # Lepton number (simplified)
    lepton_input = sum(1 for p in [p1, p2] if p in ['electron', 'muon', 'neutrino'])
    lepton_output = sum(1 for p in res if p in ['electron', 'muon', 'neutrino'])
    if lepton_input > 0 or lepton_output > 0:
        print(f"   Lepton number: {lepton_input} -> {lepton_output} {'CONSERVED' if lepton_input == lepton_output else 'CHECK'}")
    
    # Cross-section estimation (very simplified)
    print(f"\nCOLLISION PARAMETERS:")
    if te < 10:
        cross_section = "~10^-28 m^2 (very small)"
        interaction_type = "Low-energy electromagnetic"
    elif te < 100:
        cross_section = "~10^-26 m^2 (moderate)" 
        interaction_type = "Nuclear/electromagnetic"
    elif te < 1000:
        cross_section = "~10^-24 m^2 (significant)"
        interaction_type = "High-energy nuclear"
    else:
        cross_section = "~10⁻²² m² (large)"
        interaction_type = "Relativistic particle physics"
    
    print(f"   Estimated cross-section: {cross_section}")
    print(f"   Interaction regime: {interaction_type}")
    print(f"   Collision time: ~10⁻²³ seconds")
    
    print(f"\nREACTION CLASSIFICATION:")
    if "destroyed" in story.lower() or "annihilated" in story.lower():
        print("   Reaction type: ANNIHILATION")
        print(f"   Process: {p1} + {p2} → {' + '.join(res)}")
        print("   Mechanism: Matter-antimatter annihilation")
        print("   Feynman diagram: e+ + e- -> Y + Y (QED process)")
        if fmass > 0:
            print(f"   Energy release: {fmass:.1f} MeV (pure electromagnetic)")
    elif "created" in story.lower() or "made" in story.lower():
        print("   Reaction type: PARTICLE PRODUCTION")
        print(f"   Process: {p1} + {p2} → {' + '.join(res)}")
        print("   Mechanism: High-energy threshold reaction")
        if te > 1000:
            print("   Regime: Deep inelastic scattering (quark level)")
        else:
            print("   Regime: Resonance production")
    elif "bounced" in story.lower():
        print("   Reaction type: ELASTIC SCATTERING")
        print(f"   Process: {p1} + {p2} → {' + '.join(res)}")
        print("   Mechanism: Momentum transfer without particle creation")
        print("   Description: Rutherford-type scattering")
    else:
        print("   Reaction type: INELASTIC SCATTERING")
        print(f"   Process: {p1} + {p2} → {' + '.join(res)}")
        print("   Mechanism: Energy transfer with possible excitation")
    
    print(f"\n FINAL STATE PARTICLES:")
    for i, particle in enumerate(res):
        if particle in p:
            data = p[particle]
            avg_ke = (te + fmass) / len(res) if len(res) > 0 else 0
            print(f"   {i+1}. {particle}")
            print(f"      Rest mass: {data['m']:.1f} MeV/c²")
            print(f"      Charge: {data['c']:+1.0f}e")
            print(f"      Est. kinetic energy: {avg_ke:.1f} MeV")
            
            lifetimes = {
                'muon': '2.2 μs',
                'pion': '26 ns',
                'neutron': '880 s (free)',
                'kaon': '12-52 ns'
            }
            if particle in lifetimes:
                print(f"      Lifetime: {lifetimes[particle]}")
    
    print(f"\n EXPERIMENTAL CONTEXT:")
    if te < 1:
        print("   Energy scale: Atomic physics (eV range)")
        print("   Laboratory: Atomic collision experiments")
    elif te < 100:
        print("   Energy scale: Nuclear physics (MeV range)")  
        print("   Laboratory: Van de Graaff, cyclotron experiments")
    elif te < 1000:
        print("   Energy scale: High-energy nuclear (100s MeV)")
        print("   Laboratory: Linear accelerators, small synchrotrons")
    else:
        print("   Energy scale: Particle physics (GeV+ range)")
        print("   Laboratory: Large Hadron Collider, Tevatron-class")
    
    temp_kelvin = te * 1.16e10 
    print(f"   Temperature equivalent: {temp_kelvin:.1e} K")
    
    uncertainty_time = 6.58e-22 / te if te > 0 else 0 
    print(f"   Quantum uncertainty (Δt): {uncertainty_time:.1e} seconds")
    
    print(f"\n STATISTICAL ANALYSIS:")
    print(f"   Event probability: Calculated from cross-section × luminosity")
    print(f"   Background noise: Cosmic rays, detector electronics")
    print(f"   Trigger efficiency: ~85-95% for this energy range")
    print(f"   Reconstruction confidence: {85 + min(15, te/100):.0f}%")
    
    print("\n" + "="*90)
    print(" REFERENCES: Griffiths 'Particle Physics', Peskin & Schroeder 'QFT'")
    
    input("\nPress Enter to return to main menu...")

def menu():
    while True:
        print("\n" + "="*50)
        print(" Welcome to the Particle Collision Lab! ")
        print("="*50)
        print("What do you want to do?")
        print("1.  Crash two particles together")
        print("2.  Look at all available particles") 
        print("3.  Examine one particle closely")
        print("4.  Replay last collision")
        print("5.  Random collision experiment")
        print("6.  Quit")
        
        c = input("\nPick a number (1-6): ").strip()
        
        if c == "1":
            crash()
        elif c == "2":
            show()
        elif c == "3":
            look()
        elif c == "4":
            replay()
        elif c == "5":
            random_collision()
        elif c == "6":
            print("\n Thanks for playing with particles! Science is awesome! ")
            print("Remember: The universe is made of these tiny dancing particles!")
            break
        else:
            print(" That's not a choice! Pick a number from 1 to 6.")

if __name__ == "__main__":
    menu()
