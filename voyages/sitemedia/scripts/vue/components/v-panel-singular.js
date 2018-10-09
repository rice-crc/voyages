// v-panel
Vue.component('v-panel-singular', {
  props: ['title', "filters", "group", "subGroup", "align", "controlInvisible"],
  template: `
  <div class="dropdown-menu search-menu search-submenu search-menu-singular" :id="idValue" v-bind:class="dropdownMenuDirection">
    <div class="popover-content">
      <slot name="v-panel-header"></slot>
      <slot name="v-panel-content" :filters="filtersValue"></slot>
      <div class="margin-v" v-if="!controlInvisible">
        <b-button variant="info" size="sm" @click="apply">
          Apply
        </b-button>
        <b-button variant="outline-secondary" size="sm" @click="reset">
          Reset
        </b-button>
      </div>
    </div>
  </div>
  `,

  data: function() {
    return {
      titleValue: '',
      filtersValue: null,
      idValue: null,
      applyDisabled: true,
      resetDisabled: true,

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
        this.applyDisabled = (this.filters.count.changed > 0) ? false:true;
        this.resetDisabled = (this.filters.count.changed > 0 || this.filters.count.activated) ? false:true;
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
    this.filtersValue = this.filters;
  }

})
// v-panel
