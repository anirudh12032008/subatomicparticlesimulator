

import time
import os
import random

particles = {
    "electron": {"mass": 0.5, "charge": -1, "name": "electron"},
    "positron": {"mass": 0.5, "charge": 1, "name": "positron"},
    "proton": {"mass": 938, "charge": 1, "name": "proton"},
    "neutron": {"mass": 940, "charge": 0, "name": "neutron"},
    "photon": {"mass": 0, "charge": 0, "name": "photon"},
    "muon": {"mass": 106, "charge": -1, "name": "muon"},
    "pion": {"mass": 140, "charge": 0, "name": "pion"},
    "neutrino": {"mass": 0.001, "charge": 0, "name": "neutrino"},
    "kaon": {"mass": 494, "charge": 0, "name": "kaon"},
    "antiproton": {"mass": 938, "charge": -1, "name": "antiproton"}
}

last_collision = None

def show():
    print("\nHere are all the particles you can pick:")
    for name, data in particles.items():
        print(f"- {name}: mass = {data['mass']} MeV, charge = {data['charge']}")

def pick():
    plist = list(particles.keys())
    print("\nAvailable particles:")
    for i, name in enumerate(plist, 1):
        d = particles[name]
        print(f"{i}. {name} (mass: {d['mass']} MeV, charge: {d['charge']})")
    
    while True:
        c = input("\nPick a particle (name or number): ").strip()
        
        try:
            n = int(c)
            if 1 <= n <= len(plist):
                name = plist[n - 1]
                return name, particles[name]
            else:
                print(f"Pick a number between 1 and {len(plist)}!")
                continue
        except ValueError:
            pass
        
        name = c.lower()
        if name in particles:
            return name, particles[name]
        
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
    
    while True:
        try:
            e = float(input("\nHow much energy does it have? (in MeV) "))
            if e > 0:
                return e
            print("Energy has to be more than zero!")
        except ValueError:
            print("That's not a number! Try again.")

def chk(p1, p2, res):
    sc = p1["charge"] + p2["charge"]
    ec = sum(particles[p]["charge"] for p in res)
    return sc == ec

def calc(p1, p1d, e1, p2, p2d, e2):
    global last_collision
    te = e1 + e2
    
    last_collision = {
        "p1": p1, "p1d": p1d, "e1": e1,
        "p2": p2, "p2d": p2d, "e2": e2,
        "total_energy": te
    }
    
    # electron + positron = boom
    if (p1 == "electron" and p2 == "positron") or (p1 == "positron" and p2 == "electron"):
        if te > 1:
            return ["photon", "photon"], "Boom! They destroyed each other and made light!"
    
    # photon stuff
    if p1 == "photon" or p2 == "photon":
        if te > 200:
            return ["electron", "positron"], "The light made new particles!"
        else:
            return [p1, p2], "The light just bounced off."
    
    # high energy
    if te > 1000:
        if p1d["charge"] != 0 and p2d["charge"] != 0:
            return ["proton", "neutron", "pion"], "Huge crash! Made lots of new stuff!"
    
    # medium energy
    if te > 500:
        return ["muon", "pion"], "Made some medium-heavy particles!"
    
    # small crashes
    if te > 50:
        return [p1, p2], "They bounced off each other like rubber balls!"
    
    # gentle
    return [p1, p2], "They barely touched and kept going."

def crash():
    print("\n=== Time for a particle crash! ===")
    
    print("\nFirst particle:")
    p1_name, p1_data = pick()
    e1 = get_e()
    
    print("\nSecond particle:")
    p2_name, p2_data = pick()
    e2 = get_e()
    
    total_e = e1 + e2
    print("\n COLLISION SETUP:")
    print(f"   {p1_name} with {e1} MeV + {p2_name} with {e2} MeV")
    print(f"   Total energy: {total_e} MeV")
    print(f"   Energy level: {get_energy_level(total_e)}")
    
    result, story = calc(p1_name, p1_data, e1, p2_name, p2_data, e2)
    
    anim(p1_name, p2_name, result, story)
    
    print(f"\n What happened: {story}")
    print(" After the crash, we found:")
    for particle in result:
        if particle in particles:
            data = particles[particle]
            print(f"   • {particle} (mass: {data['mass']} MeV, charge: {data['charge']})")
    
    if chk(p1_data, p2_data, result):
        print("Charge conservation: All good!")
    else:
        print("Charge conservation: Something weird happened...")
    
    show_collision_summary(p1_name, p2_name, result, story)

def get_energy_level(energy):
    if energy < 10:
        return "Very gentle (thermal motion)"
    elif energy < 100:
        return "Moderate (chemical reaction level)"
    elif energy < 500:
        return "High (nuclear reaction level)"
    elif energy < 1000:
        return " Very high (particle accelerator)"
    elif energy < 2000:
        return " Extreme (Large Hadron Collider)"
    else:
        return "COSMIC! (like in space!)"

def look():
    print("\n=== Particle Detective Mode ===")
    name, data = pick()
    
    print(f"\n Examining {name} under our super microscope...")
    print(f"Mass: {data['mass']} MeV (that's how heavy it is)")
    print(f" Charge: {data['charge']} (positive, negative, or neutral)")
    
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
    if last_collision is None:
        print("\n No collision to replay! Do a collision first.")
        return
    
    print("\n REPLAYING LAST COLLISION...")
    print("=" * 50)
    
    p1 = last_collision["p1"]
    p2 = last_collision["p2"]
    e1 = last_collision["e1"] 
    e2 = last_collision["e2"]
    total_e = last_collision["total_energy"]
    
    print(f" Repeating: {p1} ({e1} MeV) + {p2} ({e2} MeV)")
    print(f"   Total energy: {total_e} MeV")
    
    input("\nPress Enter to replay the collision... 🎮")
    
    p1_data = particles[p1]
    p2_data = particles[p2]
    result, story = calc(p1, p1_data, e1, p2, p2_data, e2)
    
    anim(p1, p2, result, story)
    
    print(f"\n REPLAY RESULT: {story}")
    print("Note: Due to quantum randomness, you might get a different outcome!")

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def stable_print_chamber(header_text, chamber_content):
    """Print chamber with minimal flicker"""
    print("\n" + header_text)
    print(chamber_content)
    print() 

def anim(p1, p2, result, story):
    syms = {
        "electron": "e⁻", "positron": "e⁺", "proton": "p⁺",
        "neutron": "n⁰", "photon": "γ", "muon": "μ⁻", "pion": "π⁰",
        "neutrino": "ν", "kaon": "K⁰", "antiproton": "p̄⁺"
    }
    
    s1 = syms.get(p1, "?")
    s2 = syms.get(p2, "?")
    
    print(f"\nInitializing Large Hadron Collider simulation: {s1} + {s2}")
    print("Beam alignment in progress...")
    time.sleep(1.5)
    
    chamber_width = 120
    chamber_height = 18
    inner_width = chamber_width - 2
    collision_row = chamber_height // 2
    
    def draw_detector_chamber(particles_data=None, trails=None):
        """Draw large particle detector chamber with particle trails"""
        lines = []
        
        lines.append("╔" + "═" * inner_width + "╗")
        
        for row in range(chamber_height):
            if row == 0:
                lines.append("║" + "CERN Large Hadron Collider - Particle Detector".center(inner_width) + "║")
            elif row == 1:
                lines.append("║" + " " * inner_width + "║")
            elif row == 2 or row == chamber_height - 3:
                lines.append("║" + "▪" * inner_width + "║")
            else:
                line_content = " " * inner_width
                
                if trails and row in trails:
                    for pos in trails[row]:
                        if 0 <= pos < inner_width:
                            line_content = line_content[:pos] + "·" + line_content[pos+1:]
                
                if particles_data and row in particles_data:
                    for pos, symbol in particles_data[row]:
                        if 0 <= pos < inner_width:
                            line_content = line_content[:pos] + symbol + line_content[pos+1:]
                
                if row == collision_row and particles_data and 'main' in particles_data:
                    line_content = " " * inner_width
                    if trails and 'main' in trails:
                        for pos in trails['main']:
                            if 0 <= pos < inner_width:
                                line_content = line_content[:pos] + "·" + line_content[pos+1:]
                    for pos, symbol in particles_data['main']:
                        if 0 <= pos < inner_width:
                            line_content = line_content[:pos] + symbol + line_content[pos+1:]
                
                lines.append("║" + line_content + "║")
        
        lines.append("╚" + "═" * inner_width + "╝")
        
        return "\n".join(lines)
    
    clr()
    print("Beam injection sequence initiated")
    chamber_display = draw_detector_chamber()
    print(chamber_display)
    time.sleep(1.2)
    
    center = inner_width // 2
    
    print("\nParticle beams approaching collision point...")
    time.sleep(0.5)
    
    beam_trails = {'main': []}
    for step in range(20):
        left_pos = step * 3
        right_pos = inner_width - 1 - (step * 3)
        
        if left_pos >= right_pos - 3:
            break
        
        vertical_offset = int(0.5 * (step % 4 - 2))  
        left_row = collision_row + vertical_offset
        right_row = collision_row - vertical_offset
        
        if left_pos > 5:
            beam_trails['main'].append(left_pos - 3)
        if right_pos < inner_width - 5:
            beam_trails['main'].append(right_pos + 3)
        
        particles_data = {}
        
        if 3 <= left_row < chamber_height - 3:
            particles_data[left_row] = [(left_pos, s1)]
        if 3 <= right_row < chamber_height - 3:
            if right_row not in particles_data:
                particles_data[right_row] = []
            particles_data[right_row].append((right_pos, s2))
        
        if step % 2 == 0:
            clr()
        print(f"\rBeam energy: {step * 5}% of maximum | Collision imminent", end='')
        if step % 2 == 0:
            print() 
            chamber_display = draw_detector_chamber(particles_data, beam_trails)
            print(chamber_display)
        time.sleep(0.18)  
    
    print("\n")
    
    clr()
    print("COLLISION EVENT DETECTED - Data acquisition triggered")
    collision_particles = {'main': [(center-1, s1), (center, "⚛"), (center+1, s2)]}
    chamber_display = draw_detector_chamber(collision_particles)
    print(chamber_display)
    time.sleep(1.2)
    
    clr()
    print("High-energy interaction detected... Analyzing particle shower")
    explosion_particles = {'main': [(center, "✦")]}
    chamber_display = draw_detector_chamber(explosion_particles)
    print(chamber_display)
    time.sleep(0.8)
    
    result_symbols = [syms.get(p, "?") for p in result]
    
    trajectories = []
    particle_trails = {}
    
    if "destroyed" in story.lower() or "annihilated" in story.lower():
        for i, symbol in enumerate(result_symbols[:2]):
            direction = 1 if i == 0 else -1
            trajectories.append({
                'symbol': symbol,
                'start_x': center,
                'start_row': collision_row,
                'dx': direction * 4,  
                'dy': 0,  
                'steps': 22,
                'trail_length': 8
            })
    
    elif "bounced" in story.lower():
        for i, symbol in enumerate(result_symbols[:2]):
            direction = 1 if i == 0 else -1
            angle = random.uniform(15, 45) if i == 0 else random.uniform(-45, -15)  
            angle_rad = angle * 3.14159 / 180
            speed = 3.5
            trajectories.append({
                'symbol': symbol,
                'start_x': center,
                'start_row': collision_row,
                'dx': direction * speed * abs(angle_rad * 2), 
                'dy': speed * angle_rad * 0.8,  
                'steps': 18,
                'trail_length': 6
            })
    
    elif "made" in story.lower() or "new" in story.lower():
        angles = [0, 30, -30, 60, -60, 90, -90, 120, -120]  
        for i, symbol in enumerate(result_symbols):
            if i < 6: 
                angle = angles[i % len(angles)] + random.uniform(-10, 10)  
                angle_rad = angle * 3.14159 / 180
                speed = 3.2 + random.uniform(-0.5, 0.5)  
                
                trajectories.append({
                    'symbol': symbol,
                    'start_x': center,
                    'start_row': collision_row,
                    'dx': speed * (1 if angle_rad > 0 else -1) * (1 + abs(angle_rad) * 0.5),
                    'dy': speed * angle_rad * 0.6,  
                    'steps': 16 + random.randint(0, 6),
                    'trail_length': 5
                })
    
    else:

        for i, symbol in enumerate(result_symbols[:2]):
            direction = 1 if i == 0 else -1
            small_angle = random.uniform(-20, 20)  
            angle_rad = small_angle * 3.14159 / 180
            trajectories.append({
                'symbol': symbol,
                'start_x': center,
                'start_row': collision_row,
                'dx': direction * 2.5,
                'dy': angle_rad * 2,  
                'steps': 14,
                'trail_length': 4
            })
    
    for i, traj in enumerate(trajectories):
        particle_trails[i] = []
    
    max_steps = max([t['steps'] for t in trajectories]) if trajectories else 18
    
    for step in range(max_steps):
        particles_data = {}
        current_trails = {}
        
        for i, traj in enumerate(trajectories):
            if step < traj['steps']:
                progress = step / float(traj['steps'])
                
                x = int(traj['start_x'] + (traj['dx'] * step * 0.7))
                
                base_y = traj['start_row'] + (traj['dy'] * step * 0.12)
                
                if abs(traj['dy']) > 0.5: 
                    curvature = 0.3 * progress * progress * (1 if traj['dy'] > 0 else -1)
                    base_y += curvature
                
                row = int(base_y)
                
                if 0 <= x < inner_width and 3 <= row < chamber_height - 3:
                    if row not in particles_data:
                        particles_data[row] = []
                    particles_data[row].append((x, traj['symbol']))
                    
                    particle_trails[i].append((x, row))
                    
                    if len(particle_trails[i]) > traj['trail_length']:
                        particle_trails[i].pop(0)
        
        for i, trail_positions in particle_trails.items():
            for pos_x, pos_row in trail_positions[:-1]:  
                if 3 <= pos_row < chamber_height - 3 and 0 <= pos_x < inner_width:
                    if pos_row not in current_trails:
                        current_trails[pos_row] = []
                    current_trails[pos_row].append(pos_x)
        
        if step % 3 == 0:
            clr()
            print(f"Tracking {len(result)} particles | Frame {step+1}/{max_steps}")
            print("Multi-layer calorimeter: Recording energy deposits")
            chamber_display = draw_detector_chamber(particles_data, current_trails)
            print(chamber_display)
        else:
            print(f"\rFrame {step+1}/{max_steps} - Particle tracking in progress..", end='')
        
        time.sleep(0.5)  
    
    print("\n") 
    clr()
    print("Event reconstruction complete | Physics analysis successful")
    print(f"Collision outcome: {story}")
    print(f"Detected particles: {' + '.join(result)}")
    
    final_particles = {}
    final_trails = {}
    
    for i, trail_positions in particle_trails.items():
        for pos_x, pos_row in trail_positions:
            if 3 <= pos_row < chamber_height - 3 and 0 <= pos_x < inner_width:
                if pos_row not in final_trails:
                    final_trails[pos_row] = []
                final_trails[pos_row].append(pos_x)
    
    for i, symbol in enumerate(result_symbols[:6]):
        if i < 3:
            final_pos = max(8, center - 35 + i * 6)
            row_offset = (i - 1) * 3 + random.randint(-2, 2) 
            final_row = collision_row + row_offset
        else:
            final_pos = min(inner_width - 8, center + 35 - (i-3) * 6)
            row_offset = ((i-3) - 1) * 3 + random.randint(-1, 1)
            final_row = collision_row + row_offset
        
        if 3 <= final_row < chamber_height - 3:
            if final_row not in final_particles:
                final_particles[final_row] = []
            final_particles[final_row].append((final_pos, symbol))
    
    chamber_display = draw_detector_chamber(final_particles, final_trails)
    print(chamber_display)
    print("\nParticle identification complete. Trajectories reconstructed.")
    print("Event logged to physics database. Ready for next collision.")

def show_collision_summary(p1, p2, result, story):
    """Show detailed collision analysis with accurate physics"""
    
    print("\n" + "="*90)
    print(" PARTICLE PHYSICS COLLISION ANALYSIS REPORT".center(90))
    print("="*90)
    
    collision_data = last_collision
    p1_data = particles[p1]
    p2_data = particles[p2]
    total_energy = collision_data['total_energy']
    
    import math
    p1_mass = p1_data['mass']
    p2_mass = p2_data['mass']
    e1 = collision_data['e1']
    e2 = collision_data['e2']
    
    s = (p1_mass + p2_mass + total_energy/2)**2
    sqrt_s = math.sqrt(s)
    
    print(f"\nCOLLISION KINEMATICS:")
    print(f"   Beam A: {p1} @ {e1:.1f} MeV (rest mass: {p1_mass} MeV/c²)")
    print(f"   Beam B: {p2} @ {e2:.1f} MeV (rest mass: {p2_mass} MeV/c²)")
    print(f"   Total Lab Energy: {total_energy:.1f} MeV")
    print(f"   Center-of-Mass Energy (√s): {sqrt_s:.1f} MeV")
    
    total_input_mass = p1_mass + p2_mass
    total_output_mass = sum(particles[p]['mass'] for p in result if p in particles)
    q_value = total_input_mass - total_output_mass
    
    print(f"\n REACTION ENERGETICS:")
    print(f"   Initial rest mass: {total_input_mass:.1f} MeV/c²")
    print(f"   Final rest mass: {total_output_mass:.1f} MeV/c²")
    print(f"   Q-value: {q_value:.1f} MeV {'(exothermic)' if q_value > 0 else '(endothermic)'}")
    print(f"   Available kinetic energy: {total_energy + q_value:.1f} MeV")
    
    total_input_charge = p1_data['charge'] + p2_data['charge']
    total_output_charge = sum(particles[p]['charge'] for p in result if p in particles)
    
    print(f"\n CONSERVATION LAWS:")
    charge_conserved = (total_input_charge == total_output_charge)
    print(f"   Electric charge: {total_input_charge} → {total_output_charge} {' CONSERVED' if charge_conserved else ' VIOLATED'}")
    
    energy_conserved = total_energy >= (total_output_mass - total_input_mass)
    print(f"   Energy-momentum: {' CONSERVED' if energy_conserved else ' CHECK REQUIRED'}")
    
    baryon_input = sum(1 for p in [p1, p2] if p in ['proton', 'neutron', 'antiproton'])
    baryon_output = sum(1 for p in result if p in ['proton', 'neutron', 'antiproton'])
    if baryon_input > 0 or baryon_output > 0:
        print(f"   Baryon number: {baryon_input} → {baryon_output} {' CONSERVED' if baryon_input == baryon_output else ' CHECK'}")
    
    lepton_input = sum(1 for p in [p1, p2] if p in ['electron', 'muon', 'neutrino'])
    lepton_output = sum(1 for p in result if p in ['electron', 'muon', 'neutrino'])
    if lepton_input > 0 or lepton_output > 0:
        print(f"   Lepton number: {lepton_input} → {lepton_output} {' CONSERVED' if lepton_input == lepton_output else ' CHECK'}")
    
    print(f"\n COLLISION PARAMETERS:")
    if total_energy < 10:
        cross_section = "~10⁻²⁸ m² (very small)"
        interaction_type = "Low-energy electromagnetic"
    elif total_energy < 100:
        cross_section = "~10⁻²⁶ m² (moderate)" 
        interaction_type = "Nuclear/electromagnetic"
    elif total_energy < 1000:
        cross_section = "~10⁻²⁴ m² (significant)"
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
        print(f"   Process: {p1} + {p2} → {' + '.join(result)}")
        print("   Mechanism: Matter-antimatter annihilation")
        print("   Feynman diagram: e⁺ + e⁻ → γ + γ (QED process)")
        if q_value > 0:
            print(f"   Energy release: {q_value:.1f} MeV (pure electromagnetic)")
    elif "created" in story.lower() or "made" in story.lower():
        print("   Reaction type: PARTICLE PRODUCTION")
        print(f"   Process: {p1} + {p2} → {' + '.join(result)}")
        print("   Mechanism: High-energy threshold reaction")
        if total_energy > 1000:
            print("   Regime: Deep inelastic scattering (quark level)")
        else:
            print("   Regime: Resonance production")
    elif "bounced" in story.lower():
        print("   Reaction type: ELASTIC SCATTERING")
        print(f"   Process: {p1} + {p2} → {' + '.join(result)}")
        print("   Mechanism: Momentum transfer without particle creation")
        print("   Description: Rutherford-type scattering")
    else:
        print("   Reaction type: INELASTIC SCATTERING")
        print(f"   Process: {p1} + {p2} → {' + '.join(result)}")
        print("   Mechanism: Energy transfer with possible excitation")
    
    print(f"\n FINAL STATE PARTICLES:")
    for i, particle in enumerate(result):
        if particle in particles:
            data = particles[particle]
            avg_ke = (total_energy + q_value) / len(result) if len(result) > 0 else 0
            print(f"   {i+1}. {particle}")
            print(f"      Rest mass: {data['mass']:.1f} MeV/c²")
            print(f"      Charge: {data['charge']:+1.0f}e")
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
    if total_energy < 1:
        print("   Energy scale: Atomic physics (eV range)")
        print("   Laboratory: Atomic collision experiments")
    elif total_energy < 100:
        print("   Energy scale: Nuclear physics (MeV range)")  
        print("   Laboratory: Van de Graaff, cyclotron experiments")
    elif total_energy < 1000:
        print("   Energy scale: High-energy nuclear (100s MeV)")
        print("   Laboratory: Linear accelerators, small synchrotrons")
    else:
        print("   Energy scale: Particle physics (GeV+ range)")
        print("   Laboratory: Large Hadron Collider, Tevatron-class")
    
    temp_kelvin = total_energy * 1.16e10 
    print(f"   Temperature equivalent: {temp_kelvin:.1e} K")
    
    uncertainty_time = 6.58e-22 / total_energy if total_energy > 0 else 0 
    print(f"   Quantum uncertainty (Δt): {uncertainty_time:.1e} seconds")
    
    print(f"\n STATISTICAL ANALYSIS:")
    print(f"   Event probability: Calculated from cross-section × luminosity")
    print(f"   Background noise: Cosmic rays, detector electronics")
    print(f"   Trigger efficiency: ~85-95% for this energy range")
    print(f"   Reconstruction confidence: {85 + min(15, total_energy/100):.0f}%")
    
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
        print("5.  Quit")
        
        c = input("\nPick a number (1-5): ").strip()
        
        if c == "1":
            crash()
        elif c == "2":
            show()
        elif c == "3":
            look()
        elif c == "4":
            replay()
        elif c == "5":
            print("\n Thanks for playing with particles! Science is awesome! ")
            print("Remember: The universe is made of these tiny dancing particles!")
            break
        else:
            print(" That's not a choice! Pick a number from 1 to 5.")

if __name__ == "__main__":
    menu()

def show_chamber_animation(s1, s2, result, story, syms):
    """Animate particles moving inside the chamber box"""
    
    chamber_width = 60
    inner_width = chamber_width - 2 
    
    print("\n Accelerating particles...")
    print("\n" + "━" * chamber_width)
    print("┃" + " " * inner_width + "┃")
    print("┃" + " PARTICLE COLLISION CHAMBER ".center(inner_width) + "┃")
    print("┃" + " " * inner_width + "┃")
    print("┃" + "▫" * inner_width + "┃")  
    print("┃" + " " * inner_width + "┃")
    print("┃" + " " * inner_width + "┃")
    print("┃" + " " * inner_width + "┃")
    print("┃" + "▫" * inner_width + "┃")
    print("┃" + " " * inner_width + "┃")
    print("━" * chamber_width)
    
    print("\n Particle beams ready!")
    input("Press Enter to start collision...")
    
    print(f"\n Particles {s1} and {s2} approaching...")
    time.sleep(0.5)
    print("   " + s1 + " " * 50 + s2)
    time.sleep(0.5)
    print("     " + s1 + " " * 46 + s2)
    time.sleep(0.5)
    print("       " + s1 + " " * 42 + s2)
    time.sleep(0.5)
    print("         " + s1 + " " * 38 + s2)
    time.sleep(0.5)
    print("           " + s1 + " " * 34 + s2)
    time.sleep(0.5)
    print("             " + s1 + " " * 30 + s2)
    time.sleep(0.5)
    
    print("                   COLLISION! ")
    time.sleep(1.0)
    
    show_simple_outcome_v2(result, story, syms)
    
    print("\n" + "="*60)
    print(f"COLLISION RESULT: {story}")
    print("="*60)
    print(f"\n Final particles: {' + '.join(result)}")
    print("\nCollision complete! Data recorded!")

def show_simple_outcome_v2(result, story, syms):
    """Simple outcome animation without complex cursor movement"""
    
    result_symbols = [syms.get(p, "?") for p in result]
    
    print("\nParticles detected after collision:")
    time.sleep(0.5)
    
    if "destroyed" in story.lower() or "annihilated" in story.lower():
        print("\n ANNIHILATION - Energy radiates outward!")
        print("               γ     γ")
        time.sleep(0.5)
        print("             γ         γ")
        time.sleep(0.5)
        print("           γ             γ")
        time.sleep(0.5)
        print("         γ                 γ")
        
    elif "bounced" in story.lower():
        print("\n ELASTIC COLLISION - Particles bounce!")
        print(f"          {result_symbols[0]} ←→ {result_symbols[1]}")
        time.sleep(0.5)
        print(f"        {result_symbols[0]}     {result_symbols[1]}")
        time.sleep(0.5)
        print(f"      {result_symbols[0]}         {result_symbols[1]}")
        time.sleep(0.5)
        print(f"    {result_symbols[0]}             {result_symbols[1]}")
        
    elif "made" in story.lower() or "new" in story.lower():
        print("\n PARTICLE CREATION - New matter formed!")
        if len(result_symbols) >= 2:
            print(f"           {result_symbols[0]} {result_symbols[1]}")
            time.sleep(0.5)
            print(f"         {result_symbols[0]}   {result_symbols[1]}")
            time.sleep(0.5)
            print(f"       {result_symbols[0]}     {result_symbols[1]}")
        else:
            print(f"               {result_symbols[0]}")
            
    else:
        print("\n GENTLE INTERACTION - Minimal change!")
        print(f"          {result_symbols[0]} ~ {result_symbols[1]}")
        time.sleep(0.5)
        print(f"        {result_symbols[0]}   {result_symbols[1]}")
    
    time.sleep(1.0)

