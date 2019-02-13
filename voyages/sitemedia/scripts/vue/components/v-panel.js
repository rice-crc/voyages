template = `
    <li class="dropdown-item-li search-dropdown-item" :data-submenu-id="idValue">
        <div class="dropdown-menu-title">
          <div class="dropdown-menu-title-text">
            {{titleValue}}
          </div>
          <div class="dropdown-menu-title-count" v-if="filters.count.activated">
            <div @click="reset" class="cursor-pointer badge-count">
              <span class="badge-count-label">{{filters.count.activated}}</span>
              <span class="badge-count-btn"><i class="fa fa-times badge-btn"></i></span>
            </div>
          </div>
        </div>
        <div :id="idValue" class="search-submenu popover">
            <div class="popover-content">
              <slot name="v-panel-header"></slot>
              <slot name="v-panel-content" :filters="filtersValue" :data="data"></slot>
              <div class="margin-v">
                <b-button variant="info" size="sm" @click="apply">` +
                  gettext('Apply') +
                `</b-button>
                <b-button variant="outline-secondary" size="sm" @click="reset">` +
                  gettext('Reset') +
                `</b-button>
              </div>
            </div>
        </div>
    </li>
  `;

// v-panel
Vue.component('v-panel', {
  props: ['title', "filters", "group", "subGroup", "data"],
  template: template,

  data: function() {
    return {
      titleValue: '',
      idValue: null,
      filtersValue: null,
      resetDisabled: true,
      applyDisabled: true,
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
        this.resetDisabled = (this.filters.count.changed > 0 || this.filters.count.activated > 0) ? false:true;
        this.filtersValue = this.filters;
      },
      deep: true,
    },

  },
  created: function() { // load value initially
    this.titleValue = this.title;
    this.idValue = hyphenate(this.title);
    this.filtersValue = this.filters;
  }

})
// v-panel
