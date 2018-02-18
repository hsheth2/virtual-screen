<template>
	<div>
		<!--<div class="row">-->
		<!--<div class="col-xs-4 col-xs-offset-4">-->
		<!--<div v-if="layout.up.used" class="screen screen-used">-->
		<!--{{ layout.up.name }}-->
		<!--</div>-->
		<!--<div v-else class="screen screen-add" v-on:click="add('up')">-->
		<!--+-->
		<!--</div>-->
		<!--</div>-->
		<!--</div>-->
		<div class="row">
			<div class="col-xs-4">
				<div v-if="layout.left.used" class="screen screen-used">
					{{ layout.left.name }}
				</div>
				<div v-else class="screen screen-add" v-on:click="add('left')">
					+
				</div>
			</div>
			<div class="col-xs-4">
				<div class="screen screen-main">
					Main display
				</div>
			</div>
			<div class="col-xs-4">
				<div v-if="layout.right.used" class="screen screen-used">
					{{ layout.right.name }}
				</div>
				<div v-else class="screen screen-add" v-on:click="add('right')">
					+
				</div>
			</div>
		</div>
		<!--<div class="row">-->
		<!--<div class="col-xs-4 col-xs-offset-4">-->
		<!--<div v-if="layout.down.used" class="screen screen-used">-->
		<!--{{ layout.down.name }}-->
		<!--</div>-->
		<!--<div v-else class="screen screen-add" v-on:click="add('down')">-->
		<!--+-->
		<!--</div>-->
		<!--</div>-->
		<!--</div>-->
	</div>
</template>

<script>
	export default {
		name: "selector",
		data() {
			return {
				layout: {
					left: {},
					right: {},
					up: {},
					down: {}
				}
			}
		},
		methods: {
			add(side) {
				fetch("/addScreen", {
					method: "post", body: JSON.stringify({
						side,
						width: screen.width,
						height: screen.height
					}), headers: {
						"Content-Type": "application/json"
					}
				}).then(x => x.json()).then(res => {
					location.assign(res.address);
				})
			}
		},
		mounted() {
			fetch("/layout").then(x => x.json()).then(layout => {
				this.layout = layout;
			})
		}
	}
</script>

<style scoped>
	.screen {
		height: 30vh;
		margin: 1vh -0.1em;
		display: flex;
		justify-content: center;
		align-items: center;

		font-size: 2em;
	}

	.screen-used {
		background-color: #DDDDDD;
	}

	.screen-add {
		background-color: #7FDBFF;
		cursor: pointer;
	}

	.screen-main {
		background-color: #111111;
		color: white
	}
</style>
