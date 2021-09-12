import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}

const routes = [{
        path: '/',
        component: () => import(`@/views/Main.vue`),
        children: [
            {
                path: '',
                name: 'KnowBase',
                component: () => import(`@/components/Main/Index.vue`)
            },
            {
                path: 'musiclub',
                name: 'Music',
                component: () => import(`@/components/Main/Music.vue`)
            },
            {
                path: 'artlab',
                name: 'ArtLab',
                component: () => import(`@/components/Main/ArtLab.vue`)
            },
            {
                path: 'show',
                name: 'Show',
                component: () => import(`@/components/Main/Show.vue`)
            },
            {
                path: 'about',
                name: 'About',
                component: () => import(`@/components/Main/About.vue`)
            },
            {
                path: 'message',
                name: 'Message',
                component: () => import(`@/components/Main/Message.vue`)
            },
        ]
    },
    {
        path: '/blog',
        component: () => import(`@/views/Blog.vue`),
        redirect: {
            name: "Blog"
        },
        children: [{
                path: 'post',
                name: 'Blog',
                component: () => import(`@/components/Blog/Post.vue`)
            },
            {
                path: 'post/:id',
                name: 'BlogPost',
                component: () => import(`@/components/Blog/BlogPost.vue`),
                props: true
            },
            {
                path: 'album',
                name: 'BlogAlbum',
                component: () => import(`@/components/Blog/Album.vue`),
            },
            {
                path: 'ablum/:name',
                name: 'BlogAlbumPost',
                component: () => import(`@/components/Blog/BlogAlbumPost.vue`),
                props: true
            },
        ]
    },
    {
        path: '/sec',
        component: () => import(`@/views/Sec.vue`),
        redirect: { path: "/sec/archive" },
        children: [
            {
                path: 'archive',
                component: () => import(`@/components/Sec/Archive/Archive.vue`),
                props: true,
                children: [
                    {
                        path: '',
                        name: 'SecArchive',
                        component: () => import(`@/components/Sec/Archive/Index.vue`)
                    },
                    {
                        path: ':name',
                        name: 'SecArchiveAlbum',
                        component: () => import(`@/components/Sec/Archive/Album.vue`),
                        props: true,
                    },
                    {
                        path: ':name/:id',
                        name: 'SecArchivePaper',
                        component: () => import(`@/components/Sec/Archive/Paper.vue`),
                        props: true,
                    }
                ]
            },
        ]
    },
    // { path: '*', component: Blog }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

router.beforeEach((to, from, next) => {
    sessionStorage.setItem('referrer', from.path)
    next()
})

export default router
