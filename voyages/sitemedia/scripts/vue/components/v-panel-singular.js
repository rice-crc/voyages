// v-panel
Vue.component('v-panel-singular', {
  props: ['title', "count", "filters", "group", "subGroup"],
  template: `
  <div class="dropdown-menu search-menu search-submenu dropdown-menu-right">
    <div class="popover-content">
      <slot name="v-panel-header"></slot>
      <slot name="v-panel-content"></slot>
    </div>
  </div>
  `,

  data: function() {
    return {
      titleValue: '',
      isAdvancedValue: '',
      idValue: null,
      filtersValue: null,
      controlDisabled: true,
    }
  },

  methods: {

  },

  watch: {

  },

  mounted: function() { // load value initially
    // this.titleValue = this.title;
    // this.isAdvancedValue = this.isAdvanced;
    // this.idValue = hyphenate(this.title);
    // this.filtersValue = this.filters;
  }

})
// v-panel
