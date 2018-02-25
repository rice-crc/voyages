// v-menu-title
Vue.component('v-menu-title', {
  props: ['title', "count", "disableCaret"],
  template: `
    <a class="nav-link" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">
      <slot name="menu-title">{{title}}</slot>
      <span v-if="count">({{count}})</span>
      <i class="fa fa-caret-down" v-if="!disableCaret"></i>
    </a>
  `,
  data: function() {
    return {
    }
  },
})
// v-menu-title
