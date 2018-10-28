// v-breadcrumb
Vue.component('v-breadcrumb', {
    props: ['module', 'title', "breadcrumb", "subtitle"],
    template: `
    <div class="nav-header">
        <div>{{module}} - {{title}}</div>
        <div class="navbar-subtitle flex" v-if="subtitle">
            {{subtitle}}
        </div>
        <div class="navbar-subtitle flex" v-if="breadcrumb">
            <div class="navbar-breadcrumb" v-for="(item, index) in breadcrumb">
                <a class="v-breadcrumb-link" @click="click" :id="item.id" :alt="item.title">{{item.title}}</a><span class="navbar-breadcrumb-separator" v-if="index+1 < breadcrumb.length">-</span>
            </div>
        </div>
        <div class="navbar-padding-bottom" v-else>
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
