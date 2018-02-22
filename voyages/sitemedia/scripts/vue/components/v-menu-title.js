// v-menu-title
Vue.component('v-menu-title', {
  props: ['title', "count"],
  template: `
    <a class="nav-link" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">
      <slot name="menu-title">{{title}}</slot>
      <span v-if="count">({{count}})</span>
    </a>
  `,

  data: function() {
    return {
    }
  },

  methods: {
  },

  watch: {
  },

  mounted: function() { // load value initially
  }

})
// v-menu-title
