import * as server from "server";
import * as util from "util";
import * as childProcess from "child_process";
import {SIGKILL} from "constants";

childProcess.execSync("python3 clear_screens.py");

const {get, post} = server.router;

const screens = {
	left: {
		used: false
	},
	right: {
		used: false
	}
};

const vncServers = {
	virtual1: {
		noVNC: <childProcess.ChildProcess> null,
		vnc: <childProcess.ChildProcess> null
	},
	virtual2: {
		noVNC: <childProcess.ChildProcess> null,
		vnc: <childProcess.ChildProcess> null
	}
};

let prev = "";

server({port: 3000, security: {csrf: false}}, [
	get("/layout", ctx => {
		return screens;
	}),
	post("/addScreen", async ctx => {
		const direction = ctx.body.side;
		const x = +ctx.body.width;
		const y = +ctx.body.height;

		const stdout = childProcess.execFileSync("python3", ["create_monitor.py", direction == "left" ? "VIRTUAL1" : "VIRTUAL2" x, y, direction], {encoding: "utf8"});
		const lines = stdout.split("\n");
		const last = lines[lines.length - 1];
		console.log(last);

		childProcess.execSync(`xrandr --output eDP1 --mode 1920x1080 && xrandr ${prev} ${last}`);
		prev = last;

		if (vncServers.virtual1.vnc) {
			vncServers.virtual1.vnc.kill("SIGKILL");
		}
		if (vncServers.virtual2.vnc) {
			vncServers.virtual2.vnc.kill("SIGKILL");
		}

		if (!vncServers.virtual1.noVNC) {
			vncServers.virtual1.noVNC = childProcess.exec("./noVNC/utils/launch.sh --listen 6081 --web ./noVNC/ --vnc localhost:6071");
		}
		if (!vncServers.virtual2.noVNC) {
			vncServers.virtual2.noVNC = childProcess.exec("./noVNC/utils/launch.sh --listen 6082 --vnc localhost:6072");
		}
		const clips = JSON.parse(childProcess.execSync(`python3 get_clips_locs.py`, {encoding: "utf8"}));
		if (clips.VIRTUAL1) {
			vncServers.virtual1.vnc = childProcess.exec(`x11vnc -clip ${clips.VIRTUAL1} -rfbport 6071 -forever -cursorpos`);
		}
		if (clips.VIRTUAL2) {
			vncServers.virtual2.vnc = childProcess.exec(`x11vnc -clip ${clips.VIRTUAL2} -rfbport 6072 -forever -cursorpos`);
		}

		screens[direction].used = true;
		screens[direction].name = "Connected";

		return {
			address: `http://${ctx.headers.host}:${direction == "left" ? 6081 : 6082}/vnc_lite.html`
		}
	})
]);
