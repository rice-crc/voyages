// v-panel
Vue.component('v-panel-singular', {
  props: ['title', "count", "filters", "group", "subGroup", "align", "visible"],
  template: `
  <div class="dropdown-menu search-menu search-submenu" v-bind:class="dropdownMenuDirection">
    <div class="popover-content">
      <slot name="v-panel-header"></slot>
      <slot name="v-panel-content" :filters="filtersValue"></slot>
    </div>
  </div>
  `,

  data: function() {
    return {
      titleValue: '',
      visibleValue: '',
      filtersValue: null,
      dropdownMenuDirection: "dropdown-menu-left",
    }
  },

  methods: {
    apply() {
      this.$emit('apply', this.group, this.subGroup, this.filtersValue);
    },
    reset(group, subGroup) {
      this.$emit('reset', this.group, this.subGroup);
    }
  },

  watch: {

  },

  mounted: function() { // load value initially'd
    if (this.align == "right") {
      this.dropdownMenuDirection = "dropdown-menu-right";
    }
    this.titleValue = this.title;
    this.visibleValue = this.visible;
    this.filtersValue = this.filters;
  }

})
// v-panel
