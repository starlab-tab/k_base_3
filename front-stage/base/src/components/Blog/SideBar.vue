<template>
    <nav class="nav-0">
        <v-navigation-drawer
            v-model="drawer" 
            app permanent mini-variant 
            dark
            class="text-center"
            style="background-color: black;"
        >
            <v-btn 
                icon large dark 
                style="background-color: #367bf0; margin-top: 10px;"
                :to="{path: '/'}"
            >K</v-btn>
            <template v-slot:append>
                <v-list nav dense>
                    <v-list-item 
                        v-for="(station, index) in stations" 
                        :key="index" 
                        :to="station.route" 
                        color="#367bf0"
                        
                    >
                      <v-list-item-icon>
                        <v-icon :color="station.color">{{ station.icon }}</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title class="text-capitalize">{{ station.title }}</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                </v-list>
            </template>
        </v-navigation-drawer>
    </nav>

</template>

<script>
    export default {
        data: () => ({
            drawer: true,
            stations: [
                {
                    title: 'Album',
                    icon: 'mdi-dots-grid',
                    route: {
                        name: 'BlogAlbum'
                    }
                },
                {
                    title: 'Blog',
                    icon: 'mdi-dots-vertical',
                    route: {
                        name: 'Blog'
                    }
                },
            ],
        }),
    }
</script>

<style lang="scss" scoped>
    ::v-deep {
        .v-navigation-drawer__border {
                // box-shadow: inset -15px 0px 10px -18px #367bf0;
                // filter: blur(8px);
                // background-color: #367bf0!important;
                // width: 8px;
                // background-color: unset!important;
        }
    }
</style>
