// v-panel
Vue.component('v-panel-singular', {
  props: ['title', "filters", "group", "subGroup", "align"],
  template: `
  <div class="dropdown-menu search-menu search-submenu" :id="idValue" v-bind:class="dropdownMenuDirection">
    <div class="popover-content">
      <slot name="v-panel-header"></slot>
      <slot name="v-panel-content" :filters="filtersValue"></slot>
      <div class="margin-v">
        <b-button :disabled="controlDisabled" variant="info" size="sm" @click="apply">
          Apply
        </b-button>
        <b-button :disabled="controlDisabled" variant="outline-secondary" size="sm" @click="reset">
          Reset
        </b-button>
      </div>
    </div>
  </div>
  `,

  data: function() {
    return {
      titleValue: '',
      visibleValue: '',
      filtersValue: null,
      idValue: null,
      controlDisabled: true,

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
    filters: {
      handler: function(){
        this.controlDisabled = (this.filters.count.changed > 0) ? false:true;
      },
      deep: true,
    },
  },

  created: function() { // load value initially'd
    if (this.align == "right") {
      this.dropdownMenuDirection = "dropdown-menu-right";
    }
    this.idValue = hyphenate(this.title);
    this.titleValue = this.title;
    this.visibleValue = this.visible;
    this.filtersValue = this.filters;
  }

})
// v-panel
