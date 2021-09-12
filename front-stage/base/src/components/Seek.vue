<template>
    <div class="text-center">
        <v-dialog v-model="dialog" :fullscreen="isFullDialog" overlay-opacity=0.15 width="45%" scrollable>
            <!--      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="red lighten-2"
          dark
          v-bind="attrs"
          v-on="on"
        >
          Click Me
        </v-btn>
      </template> -->
            <v-card color="white">
                <v-card-title class="headline grey lighten-2 pa-0" style="height: 4rem;">
                    <v-row no-gutters class="px-0 align-center">
                        <v-col style="max-width: fit-content;" class="pl-1">
                            <v-menu open-on-hover transition="slide-x-transition" offset-y>
                                <template v-slot:activator="{ attrs, on }">
                                    <v-btn class="grey lighten-2 primary--text px-0" v-bind="attrs" v-on="on" depressed>
                                        <v-icon :color="seekSta.color">{{ seekSta.icon }}</v-icon>
                                    </v-btn>
                                </template>

                                <v-list>
                                    <v-list-item v-for="station in space" :key="station.title" class="justify-center"
                                        link @click="stationSwitch(station)">
                                        <v-icon :color="station.color">{{ station.icon }}</v-icon>
                                    </v-list-item>
                                </v-list>
                            </v-menu>
                        </v-col>
                        <v-col>
                            <v-text-field solo hide-details clearable flat autofocus background-color="grey lighten-2"
                                @click:clear="clearSeekText" v-model="seekText"></v-text-field>
                        </v-col>
                    </v-row>
                </v-card-title>

                <v-card-text>
                    <v-row class="mt-4">
                        <v-col cols="12" v-for="(item, index) in seekItems" :key="index" class="pb-2">
                            <v-hover v-slot="{ hover }">
                                <v-card link :elevation="hover ? 1 : 0" :class="{ 'on-hover': hover }"
                                    class="seek-card grey lighten-4">
                                    <v-card-subtitle class="pt-2 pb-0 black--text font-weight-medium">
                                        {{ item.title }}
                                    </v-card-subtitle>
                                    <v-card-text class="row-2 pt-2 pb-0 d-inline-block text-truncate text-wrap">
                                        {{ item.desc }}
                                    </v-card-text>
                                </v-card>
                            </v-hover>
                        </v-col>
                    </v-row>
                </v-card-text>

            </v-card>
        </v-dialog>
    </div>
</template>

<script>
    export default {
        props: [
            'space'
        ],
        data() {
            return {
                dialog: false,
                seekSta: this.space[0],
                seekText: "",
                seekItems: [{
                        title: "vulnhub靶机渗透[GoatseLinux-1]",
                        desc: "泛分发。这是专门为VMware 6.5兼容性而构建的。警告：GoatseLinux是不安全的。 它被设计为用于进行渗透测试的实验室工具箱。 由于几乎所有安装的程序都具有广泛的开放性，因此强烈建议您不要..."
                    },
                    {
                        title: "reverse shell 大全",
                        desc: "现在，本地侦听服务器中键入的所有内容都将在目标上执行，并且命令的输出将通过管道返回。请记住，我们不在目标上使用任何第三方工具，而是在其默认shell程序上使用。该技术在许多情况下都很"
                    },
                    {
                        title: "Hack-The-Box-walkthrough[ServMon]",
                        desc: "介绍操作系统：Windows难度：容易点数：20发行：2020年4月11日IP：10.10.10.184 user一血用时：3小时08分钟06秒。root一血用时：3小时34分钟10秒。"
                    },
                    {
                        title: "lxd容器提权",
                        desc: "介绍LXD是Ubuntu的使用linux容器的容器管理器。可以认为它与docker在同一领域内发挥作用， 应该将lxd组视为与docker组危害方式相同。在任何情况下，都不应授予本地容器中的用户访问"
                    },
                    {
                        title: "vulnhub靶机渗透[SkyTower-1]",
                        desc: "的网站，并抓包分析 email参数容易受到SQL注入的攻击。 但是使用sqlmap等自动化sql注入测试工具无法跑出数据，因为对sql注入语句做了过滤，需要想办法寻找payload绕过 多..."
                    },
                    {
                        title: "vulnhub靶机渗透[SickOs-1-1",
                        desc: "扫描期间观察到3128上存在有关代理的内容，那么尝试在firefox浏览器中手动建立代理。在HTTP代理和端口3128中提供VM的IP，如下图所示： 访问robotx.txt文件，查看里面的内容..."
                    },
                    {
                        title: "LaZagne---全平台多功能密码恢复工具",
                        desc: ""
                    },
                    {
                        title: "all-things-about-ctf",
                        desc: "注册就是一道坎，里面难的机器能难飞天，最容易的机器，要拿下也需要一段时间"
                    },
                    {
                        title: "炸药制造(deep web)",
                        desc: "到20度以下。差点忘记说了，冬季可能比较容易，夏秋季节的话，呵呵，那还是准备一些冰块吧。"
                    },
                    {
                        title: "shellshock漏洞运作原理分析及其利用",
                        desc: "quot; 在终端中运行以上行显示是否容易受到Shellshock的攻击。如果输出中显示“shellshocked”，则说明很容易受到shellshock攻击，现在该进行更新了"
                    }
                ]
            }
        },
        computed: {
            isFullDialog: function() {
                switch (this.$vuetify.breakpoint.name) {
                    case 'xs':
                        return true
                    default:
                        return false
                }
            },
        },
        methods: {
            stationSwitch: function(sta) {
                this.seekSta = sta
            },
            clearSeekText: function() {
                if (this.isFullDialog) {
                    this.dialog = false
                }
            },
            callSeek: function() {
                this.dialog = !this.dialog
            }
        }
    }
</script>

<style scoped>
    .seek-card:not(.on-hover) {
        transition: opacity .4s ease-in-out;
        /* opacity: 1; */
    }
</style>
