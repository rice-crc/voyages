// v-breadcrumb
Vue.component('v-breadcrumb', {
    props: ['module', 'title', "breadcrumb"],
    template: `
    <div class="nav-header">
        <div>{{module}} - {{title}}</div>
        <div class="navbar-subtitle flex">
            <div class="navbar-breadcrumb" v-for="(item, index) in breadcrumb">
                <a href class="v-breadcrumb-link" @click="click" :id="item.id" :alt="item.title">{{item.title}}</a><span class="navbar-breadcrumb-separator" v-if="index+1 < breadcrumb.length">-</span>
            </div>
        </div>
    </div>
  `,

    data: function () {
        return {
        }
    },

    methods: {
        click(event) {
            this.$emit('clicked', event.target.id);
        }
    },

    watch: {

    },
    created: function () { // load value initially
    }

})
// v-breadcrumb
