// v-panel
Vue.component('v-panel', {
  props: ['title', "count", "filters", "isAdvanced", "group", "subGroup"],
  template: `
    <li v-if="isAdvancedValue" class="dropdown-item dropdown-item-li search-dropdown-item" :data-submenu-id="idValue">
        <div class="dropdown-menu-title">
          <div class="dropdown-menu-title-text">
            {{titleValue}}
          </div>
          <div class="dropdown-menu-title-count">
            <b-badge variant="danger" v-if="count">{{count}}</b-badge>
          </div>
        </div>
        <div :id="idValue" class="search-submenu popover">
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
    </li>
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
    apply() {
      this.$emit('apply', this.group, this.subGroup, this.filtersValue);
    },
    reset(group, subGroup) {
      this.$emit('reset', this.group, this.subGroup);
    }
  },

  watch: {
    count: {
      handler: function(){
        this.controlDisabled = (this.count.changed > 0) ? false:true;
      },
      deep: true,
    }
  },

  mounted: function() { // load value initially
    this.titleValue = this.title;
    this.isAdvancedValue = this.isAdvanced;
    this.idValue = hyphenate(this.title);
    this.filtersValue = this.filters;
  }

})
// v-panel
