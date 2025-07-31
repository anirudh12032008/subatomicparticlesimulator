from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
import time
import os
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
import queue
import uuid


import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xyz'
socketio = SocketIO(app, cors_allowed_origins="*")


active_sessions = {}


class Tsess:
    def __init__(self, sesid, clntid):
        self.sesid = sesid
        self.clntid = clntid
        self.inque = queue.Queue()
        self.outque = queue.Queue()
        self.waitinp = False
        self.currprompt = ""
        self.inpbuff = ""
        self.simthread = None
        self.running = True

    def write_output(self, text):
        self.outque.put(text)
        socketio.emit('terminal_output', text, to=self.clntid)

    def request_input(self, prompt=""):
        self.currprompt = prompt
        self.waitinp = True
        if prompt:
            self.write_output(prompt)

    def provide_input(self, data):
        if self.waitinp:
            self.inque.put(data.strip())
            self.waitinp = False

    def get_input(self, prompt=""):
        self.request_input(prompt)
        while self.running:
            try:
                result = self.inque.get(timeout=0.1)
                return result
            except queue.Empty:
                continue
        return ""


class WebTerminalIO:
    def __init__(self, session):
        self.session = session

    def write(self, text):

        if '\n' in text and '\r\n' not in text:
            text = text.replace('\n', '\r\n')
        self.session.write_output(text)

    def flush(self):
        pass


def create_web_input(session):
    def web_input(prompt=""):
        return session.get_input(prompt)
    return web_input


def run_simulator_menu(session):

    import builtins
    original_input = builtins.input

    try:

        web_io = WebTerminalIO(session)

        builtins.input = create_web_input(session)

        with redirect_stdout(web_io):

            print("IF THIS DOESNT WORKS PLEASE TRY THE BUILD FILE FROM THE GITHUB REPO INSTEAD")
            time.sleep(1.5)
            print("\n Initializing CERN Particle Physics Laboratory...")
            time.sleep(0.8)
            print("Loading Large Hadron Collider simulation...")
            time.sleep(0.6)
            print("Configuring particle beam systems...")
            time.sleep(0.5)
            print("Calibrating detectors...")
            time.sleep(0.4)
            print("Physics engine ready!\n")
            time.sleep(0.3)

            print("Testing chamber display:")
            print("+" + "-"*50 + "+")
            print("|" + " "*50 + "|")
            print("|" + "  CERN Particle Detector".center(50) + "|")
            print("|" + " "*50 + "|")
            print("+" + "-"*50 + "+")
            print("")

            main.menu()

    except Exception as e:
        session.write_output(
            f'\r\n\x1b[31mError in simulator: {str(e)}\x1b[0m\r\n')
    finally:

        builtins.input = original_input
        session.running = False


@app.route('/')
def index():
    return render_template('terminal.html')


client_sessions = {}


@socketio.on('connect')
def handle_connect():
    sesid = str(uuid.uuid4())
    clntid = request.sid

    session = Tsess(sesid, clntid)
    active_sessions[sesid] = session
    client_sessions[clntid] = sesid

    session.simthread = threading.Thread(
        target=run_simulator_menu,
        args=(session,),
        daemon=True
    )
    session.simthread.start()


@socketio.on('disconnect')
def handle_disconnect():

    clntid = request.sid
    if clntid in client_sessions:
        sesid = client_sessions[clntid]
        if sesid in active_sessions:
            active_sessions[sesid].running = False
            del active_sessions[sesid]
        del client_sessions[clntid]


@socketio.on('terminal_input')
def handle_terminal_input(data):

    clntid = request.sid
    if clntid in client_sessions:
        sesid = client_sessions[clntid]
        if sesid in active_sessions:
            session = active_sessions[sesid]

            if data == '\r' or data == '\n':

                session.write_output('\r\n')
                session.provide_input(session.inpbuff)
                session.inpbuff = ""
            elif data == '\x7f' or data == '\b':

                if session.inpbuff:
                    session.inpbuff = session.inpbuff[:-1]
                    session.write_output('\b \b')
            elif data == '\x03':

                session.write_output('\r\n^C\r\n')
                session.provide_input("")
                session.inpbuff = ""
            elif ord(data) >= 32:

                session.inpbuff += data
                session.write_output(data)


def patchmod():
    import shutil
    def webclr():
        print('\033[2J\033[1;1H', end='', flush=True)

    def getsize(fallback=(80, 24)):
        import collections
        terminal_size = collections.namedtuple(
            'terminal_size', ['columns', 'lines'])
        return terminal_size(100, 24)

    if hasattr(main, 'anim'):

        original_anim = main.anim

        def web_anim(p1, p2, result, story):
            syms = {
                "electron": "e-", "positron": "e+", "proton": "p+",
                "neutron": "n0", "photon": "Y", "muon": "u-", "pion": "pi",
                "neutrino": "v", "kaon": "K0", "antiproton": "p-"
            }

            s1 = syms.get(p1, "?")
            s2 = syms.get(p2, "?")

            print(
                f"Initializing Large Hadron Collider simulation: {s1} + {s2}")
            print("Beam alignment in progress...")
            time.sleep(1.5)

            webclr()
            print("Beam injection sequence initiated")

            print("+" + "="*60 + "+")
            print("|" + "CERN Large Hadron Collider - Particle Detector".center(60) + "|")
            print("|" + " "*60 + "|")
            print("|" + "."*60 + "|")
            print("|" + " "*60 + "|")
            print("|" + " "*60 + "|")
            print("|" + " "*60 + "|")
            print("|" + "."*60 + "|")
            print("|" + " "*60 + "|")
            print("+" + "="*60 + "+")

            time.sleep(1.2)

            print("\nParticle beams approaching collision point...")
            time.sleep(0.5)

            for step in range(10):
                webclr()
                print(
                    f"Beam energy: {step * 10}% of maximum | Collision imminent")

                left_spaces = " " * (step * 2)
                right_spaces = " " * (step * 2)
                middle_spaces = " " * \
                    max(0, 60 - len(left_spaces) -
                        len(right_spaces) - len(s1) - len(s2))

                print("+" + "="*60 + "+")
                print(
                    "|" + "CERN Large Hadron Collider - Particle Detector".center(60) + "|")
                print("|" + " "*60 + "|")
                print("|" + "."*60 + "|")
                print("|" + " "*60 + "|")
                print("|" + left_spaces + s1 +
                      middle_spaces + s2 + right_spaces + "|")
                print("|" + " "*60 + "|")
                print("|" + "."*60 + "|")
                print("|" + " "*60 + "|")
                print("+" + "="*60 + "+")

                time.sleep(0.3)

                if step >= 8:
                    break

            webclr()
            print("COLLISION EVENT DETECTED - Data acquisition triggered")

            print("+" + "="*60 + "+")
            print("|" + "CERN Large Hadron Collider - Particle Detector".center(60) + "|")
            print("|" + " "*60 + "|")
            print("|" + "."*60 + "|")
            print("|" + " "*60 + "|")
            print("|" + " "*25 + "*** BOOM ***" + " "*23 + "|")
            print("|" + " "*60 + "|")
            print("|" + "."*60 + "|")
            print("|" + " "*60 + "|")
            print("+" + "="*60 + "+")

            print(f"\nCollision complete: {s1} + {s2} -> {story}")
            time.sleep(2)

        main.anim = web_anim

    main.clr = webclr
    shutil.get_terminal_size = getsize


patchmod()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0',
                 port=8081, allow_unsafe_werkzeug=True)
