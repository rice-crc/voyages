// v-menu-title
Vue.component('v-menu-title', {
  props: ['title', "count", "disableCaret"],
  template: `
    <a class="nav-link" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false" @mouseover="activate" @click="activate">
      <slot name="menu-title">{{title}}</slot>
      <span v-if="count.activated">({{count.activated}})</span>
      <i class="fa fa-caret-down" v-if="!disableCaret"></i>
    </a>
  `,
  data: function() {
    return {
    }
  },
  methods: {
    activate: function() {
      // activate the first row by default upon expansion
      this.$el.click();
      var firstRow = this.$el.parentElement.lastElementChild.children[0].children[0];
      if (this.$el.parentElement.lastElementChild.children[0].children[0].tagName == "LI") {
        activateSubmenu(firstRow);
      }
    }
  }
})
// v-menu-title
