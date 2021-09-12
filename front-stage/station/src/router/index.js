import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        component: () => import(`@/views/Home.vue`),
        meta: {
            free: true
        },
    },
    {
        path: '/bridge',
        name: 'Bridge',
        component: () => import(`@/views/Bridge.vue`),
        meta: {
            free: true
        },
    },
    {
        path: '/winterfell',
        name: 'WinterFell',
        redirect: { name: "Dashbord" },
        component: () => import(`@/views/Base.vue`),
        children: [
            {
              path: 'dashbord',
              name: 'Dashbord',
              component: () => import(`@/components/Dashbord/Dashbord.vue`),
            },
            {
                path: 'blog',
                name: 'Blog',
                component: () => import(`@/components/Global/Layout.vue`),
                redirect: { name: "BlogPost" },
                children: [
                    {
                        path: "post",
                        name: "BlogPost",
                        component: () =>
                        import(
                          `@/components/Blog/Post.vue`
                        )
                    },
                    {
                        path: "album",
                        name: "BlogAlbum",
                        component: () =>
                        import(
                          `@/components/Blog/Album.vue`
                        )
                    },
                    {
                        path: "post/edit/:id",
                        name: "BlogEdit",
                        component: () =>
                        import(
                          `@/components/Blog/Edit.vue`
                        ),
                        props: true
                    },
                    {
                        path: "post/create",
                        name: "BlogCreate",
                        component: () =>
                        import(
                          `@/components/Blog/Create.vue`
                        )
                    },
                ]
            },
            {
                path: 'art',
                component: () => import(`@/components/Global/Layout.vue`),
                children: [
                    {
                      path: '',
                      name: 'Art',
                      component: () => import(`@/components/Art/Art.vue`),  
                    },
                ]
            },
            {
                path: 'show',
                component: () => import(`@/components/Global/Layout.vue`),
                children: [
                    {
                      path: '',
                      name: 'Show',
                      component: () => import(`@/components/Show/Show.vue`),  
                    },
                ]
            },
            {
                path: 'sec',
                name: 'Sec',
                component: () => import(`@/components/Global/Layout.vue`),
                redirect: { name: "SecArchivePaper" },
                children: [
                    {
                      path: "archive/paper",
                      name: "SecArchivePaper",
                      component: () =>
                        import(
                          `@/components/Sec/Archive/Paper.vue`
                        )
                    },
                    {
                      path: "archive/album",
                      name: "SecArchiveAlbum",
                      component: () =>
                        import(
                          `@/components/Sec/Archive/Album.vue`
                        )
                    },
                    {
                      path: "archive/crawler",
                      name: "SecArchiveCrawler",
                      component: () =>
                        import(
                          `@/components/Sec/Archive/Crawler.vue`
                        )
                    },
                    {
                      path: "archive/manual",
                      name: "SecArchiveManual",
                      component: () =>
                        import(
                          `@/components/Sec/Archive/Manual.vue`
                        )
                    },
                    {
                      path: "archive/edit/:id",
                      name: "SecArchiveEdit",
                      component: () =>
                        import(
                          `@/components/Sec/Archive/Edit.vue`
                        ),
                      props: true
                    },
                    {
                      path: "vuln",
                      name: "SecVuln",
                      component: () =>
                        import(
                          `@/components/Sec/Vuln.vue`
                        )
                    },
                ]
            },
            {
                path: 'message',
                name: 'Message',
                component: () => import(`@/components/Global/Layout.vue`),
                children: [
                    {
                      path: "main",
                      name: "MessageMain",
                      component: () =>
                        import(
                          `@/components/Message/Main.vue`
                        )
                    },
                    {
                      path: "chat",
                      name: "Chat",
                      component: () =>
                        import(
                          `@/components/Message/Chat.vue`
                        )
                    },
                    {
                      path: "email",
                      name: "Email",
                      component: () =>
                        import(
                          `@/components/Message/Email.vue`
                        )
                    },
                ]
            },
        ]
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

router.beforeEach((to, from, next) => {
    let key = localStorage.getItem("language") ? true : false
    if (!key) {
        if (!to.meta.free) return next({ path: '/' })
        return next()
    }
    else {
        if (to.meta.free) return next({name: 'Dashbord'})
        else return next()
    }
})
router.afterEach(() => {})

export default router
