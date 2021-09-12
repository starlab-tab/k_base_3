<template>
    <v-container justify-center fluid fill-height align-start style="background-color:#f9f7f1">
        <v-row id="about-view">
            <v-col cols="12" class="d-flex justify-center align-center" style="height: 240px;">
           <v-avatar
                size="160"
            >
                <img src="@/assets/arya.png"/>
            </v-avatar>
            </v-col>
            <v-col cols="12">
                <ul class="quotes">
                    <li v-for="i in 1" :key="i" class="quote">
                        <span class="title">
                            From the TV Series: 
                            <a href="https://www.moviequotes.com/s-tv-series/game-of-thrones/" target="_blank">GAME OF THRONES</a>
                        </span>
                        <div class="content text-end">
                            <blockquote class="text-start">
                                “My fight is with the Authority...
..and those doling out cruelties in his name...
..those who seek to divide in order to control...
..and who have built worlds founded on privilege and divine right
rather than care and need.
I fight for freedom of knowledge,
and in place of deceit, intolerance and prejudice...
..I fight for the possibilities of
understanding, truth and acceptance.
But I cannot win these things alone.
I will need help and support.
From you, and all those who have rebelled.
Let us be united in heart, soul and deed, and together we could build a Republic of Heaven above and a Republic of Ideas below.
Worlds in which the scars of history may be healed.
Better worlds, where the privilege of freedom becomes the right of all peoples.”
                            </blockquote>
                            <span>
                                <time>[ 0:42:43.30 - 0:42:47.55 ]</time>
                                <cite>
                                    <a href="https://www.moviequotes.com/quotes-by/lena-headey/" target="_blank">Lena Headey</a>
                                    - Cersei Lannister
                                </cite>
                            </span>
                        </div>
                    </li>
                    
                </ul>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    // import Viewer from '@/plugins/viewer.js';
    export default {
        props: ['id'],
        data: () => ({
            
        }),
        mounted() {
            // const viewer = new Viewer(document.getElementById('about-view'))
        },
    }
</script>

<style lang="scss" scoped>
    .quotes {
        margin: auto;
        width: 60%;
        padding: 0;
        list-style: none;
        border-radius: 0.25rem;
        @media only screen and (max-width: 768px) {
            width: 100%!important;
            blockquote {
                font-size: 1rem!important;
            }
        }
        .quote {    
            padding: 0 0 0 1rem;
            border-left: 0.375rem solid #DA7517;
            margin: 4rem 0;
        }
        a {
            text-decoration: none;
            &:hover {
                text-decoration: underline;
            }
        }
        .title {
            font-size: .7rem!important;
            font-weight: bold;
            color: #999;
            a {
                color: #999;color: #999;
                text-transform: uppercase;
            }
        }
        .content {
            blockquote {
                padding: 8px 0;
                font-size: 1.4rem;
                font-style: italic;
                color: #444;
            }
            span {
                display: grid;
                font-size: .8rem;
                color: #444;
                font-style: italic;
                time {
                    color: #999;
                }
                cite {
                    a {
                        text-transform: uppercase;
                        color: #DA7517;
                    }
                }
            }
        }
    }
</style>
