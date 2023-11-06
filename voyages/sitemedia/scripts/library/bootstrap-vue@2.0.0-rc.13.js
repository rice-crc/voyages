(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = global || self, global.bootstrapVue = factory());
}(this, function () { 'use strict';

  function _typeof(obj) {
    if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") {
      _typeof = function (obj) {
        return typeof obj;
      };
    } else {
      _typeof = function (obj) {
        return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
      };
    }

    return _typeof(obj);
  }

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];
      descriptor.enumerable = descriptor.enumerable || false;
      descriptor.configurable = true;
      if ("value" in descriptor) descriptor.writable = true;
      Object.defineProperty(target, descriptor.key, descriptor);
    }
  }

  function _createClass(Constructor, protoProps, staticProps) {
    if (protoProps) _defineProperties(Constructor.prototype, protoProps);
    if (staticProps) _defineProperties(Constructor, staticProps);
    return Constructor;
  }

  function _defineProperty(obj, key, value) {
    if (key in obj) {
      Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
      });
    } else {
      obj[key] = value;
    }

    return obj;
  }

  function _objectSpread(target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i] != null ? arguments[i] : {};
      var ownKeys = Object.keys(source);

      if (typeof Object.getOwnPropertySymbols === 'function') {
        ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) {
          return Object.getOwnPropertyDescriptor(source, sym).enumerable;
        }));
      }

      ownKeys.forEach(function (key) {
        _defineProperty(target, key, source[key]);
      });
    }

    return target;
  }

  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function");
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        writable: true,
        configurable: true
      }
    });
    if (superClass) _setPrototypeOf(subClass, superClass);
  }

  function _getPrototypeOf(o) {
    _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) {
      return o.__proto__ || Object.getPrototypeOf(o);
    };
    return _getPrototypeOf(o);
  }

  function _setPrototypeOf(o, p) {
    _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) {
      o.__proto__ = p;
      return o;
    };

    return _setPrototypeOf(o, p);
  }

  function _assertThisInitialized(self) {
    if (self === void 0) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }

    return self;
  }

  function _possibleConstructorReturn(self, call) {
    if (call && (typeof call === "object" || typeof call === "function")) {
      return call;
    }

    return _assertThisInitialized(self);
  }

  function _toConsumableArray(arr) {
    return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _nonIterableSpread();
  }

  function _arrayWithoutHoles(arr) {
    if (Array.isArray(arr)) {
      for (var i = 0, arr2 = new Array(arr.length); i < arr.length; i++) arr2[i] = arr[i];

      return arr2;
    }
  }

  function _iterableToArray(iter) {
    if (Symbol.iterator in Object(iter) || Object.prototype.toString.call(iter) === "[object Arguments]") return Array.from(iter);
  }

  function _nonIterableSpread() {
    throw new TypeError("Invalid attempt to spread non-iterable instance");
  }

  var __assign=function(){return (__assign=Object.assign||function(e){for(var a,s=1,t=arguments.length;s<t;s++)for(var r in a=arguments[s])Object.prototype.hasOwnProperty.call(a,r)&&(e[r]=a[r]);return e}).apply(this,arguments)};function mergeData(){for(var e,a,s={},t=arguments.length;t--;)for(var r=0,c=Object.keys(arguments[t]);r<c.length;r++)switch(e=c[r]){case"class":case"style":case"directives":Array.isArray(s[e])||(s[e]=[]),s[e]=s[e].concat(arguments[t][e]);break;case"staticClass":if(!arguments[t][e])break;void 0===s[e]&&(s[e]=""),s[e]&&(s[e]+=" "),s[e]+=arguments[t][e].trim();break;case"on":case"nativeOn":s[e]||(s[e]={});for(var n=0,o=Object.keys(arguments[t][e]||{});n<o.length;n++)a=o[n],s[e][a]?s[e][a]=[].concat(s[e][a],arguments[t][e][a]):s[e][a]=arguments[t][e][a];break;case"attrs":case"props":case"domProps":case"scopedSlots":case"staticStyle":case"hook":case"transition":s[e]||(s[e]={}),s[e]=__assign({},arguments[t][e],s[e]);break;case"slot":case"key":case"ref":case"tag":case"show":case"keepAlive":default:s[e]||(s[e]=arguments[t][e]);}return s}

  var props = {
    disabled: {
      type: Boolean,
      default: false
    },
    ariaLabel: {
      type: String,
      default: 'Close'
    },
    textVariant: {
      type: String,
      default: null
    } // @vue/component

  };
  var BButtonClose = {
    name: 'BButtonClose',
    functional: true,
    props: props,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          listeners = _ref.listeners,
          slots = _ref.slots;
      var componentData = {
        staticClass: 'close',
        class: _defineProperty({}, "text-".concat(props.textVariant), props.textVariant),
        attrs: {
          type: 'button',
          disabled: props.disabled,
          'aria-label': props.ariaLabel ? String(props.ariaLabel) : null
        },
        on: {
          click: function click(e) {
            // Ensure click on button HTML content is also disabled
            if (props.disabled && e instanceof Event) {
              e.stopPropagation();
              e.preventDefault();
            }
          }
        } // Careful not to override the default slot with innerHTML

      };

      if (!slots().default) {
        componentData.domProps = {
          innerHTML: '&times;'
        };
      }

      return h('button', mergeData(data, componentData), slots().default);
    }
  };

  var BAlert = {
    name: 'BAlert',
    components: {
      BButtonClose: BButtonClose
    },
    model: {
      prop: 'show',
      event: 'input'
    },
    props: {
      variant: {
        type: String,
        default: 'info'
      },
      dismissible: {
        type: Boolean,
        default: false
      },
      dismissLabel: {
        type: String,
        default: 'Close'
      },
      show: {
        type: [Boolean, Number],
        default: false
      },
      fade: {
        type: Boolean,
        default: false
      }
    },
    data: function data() {
      return {
        countDownTimerId: null,
        dismissed: false
      };
    },
    computed: {
      classObject: function classObject() {
        return ['alert', this.alertVariant, this.dismissible ? 'alert-dismissible' : ''];
      },
      alertVariant: function alertVariant() {
        var variant = this.variant;
        return "alert-".concat(variant);
      },
      localShow: function localShow() {
        return !this.dismissed && (this.countDownTimerId || this.show);
      }
    },
    watch: {
      show: function show() {
        this.showChanged();
      }
    },
    mounted: function mounted() {
      this.showChanged();
    },
    destroyed
    /* istanbul ignore next */
    : function destroyed() {
      this.clearCounter();
    },
    methods: {
      dismiss: function dismiss() {
        this.clearCounter();
        this.dismissed = true;
        this.$emit('dismissed');
        this.$emit('input', false);

        if (typeof this.show === 'number') {
          this.$emit('dismiss-count-down', 0);
          this.$emit('input', 0);
        } else {
          this.$emit('input', false);
        }
      },
      clearCounter: function clearCounter() {
        if (this.countDownTimerId) {
          clearInterval(this.countDownTimerId);
          this.countDownTimerId = null;
        }
      },
      showChanged: function showChanged() {
        var _this = this;

        // Reset counter status
        this.clearCounter(); // Reset dismiss status

        this.dismissed = false; // No timer for boolean values

        if (this.show === true || this.show === false || this.show === null || this.show === 0) {
          return;
        } // Start counter (ensure we have an integer value)


        var dismissCountDown = parseInt(this.show, 10) || 1;
        this.countDownTimerId = setInterval(function () {
          if (dismissCountDown < 1) {
            _this.dismiss();

            return;
          }

          dismissCountDown--;

          _this.$emit('dismiss-count-down', dismissCountDown);

          _this.$emit('input', dismissCountDown);
        }, 1000);
      }
    },
    render: function render(h) {
      if (!this.localShow) {
        // If not showing, render placeholder
        return h(false);
      }

      var dismissBtn = h(false);

      if (this.dismissible) {
        // Add dismiss button
        dismissBtn = h('b-button-close', {
          attrs: {
            'aria-label': this.dismissLabel
          },
          on: {
            click: this.dismiss
          }
        }, [this.$slots.dismiss]);
      }

      var alert = h('div', {
        class: this.classObject,
        attrs: {
          role: 'alert',
          'aria-live': 'polite',
          'aria-atomic': true
        }
      }, [dismissBtn, this.$slots.default]);
      return !this.fade ? alert : h('transition', {
        props: {
          name: 'fade',
          appear: true
        }
      }, [alert]);
    }
  };

  /**
   * Register a component plugin as being loaded. returns true if component plugin already registered
   * @param {object} Vue
   * @param {string} Component name
   * @param {object} Component definition
   */
  function registerComponent(Vue, name, def) {
    Vue._bootstrap_vue_components_ = Vue._bootstrap_vue_components_ || {};
    var loaded = Vue._bootstrap_vue_components_[name];

    if (!loaded && def && name) {
      Vue._bootstrap_vue_components_[name] = true;
      Vue.component(name, def);
    }

    return loaded;
  }
  /**
   * Register a group of components as being loaded.
   * @param {object} Vue
   * @param {object} Object of component definitions
   */

  function registerComponents(Vue, components) {
    for (var component in components) {
      registerComponent(Vue, component, components[component]);
    }
  }
  /**
   * Register a directive as being loaded. returns true if directive plugin already registered
   * @param {object} Vue
   * @param {string} Directive name
   * @param {object} Directive definition
   */

  function registerDirective(Vue, name, def) {
    Vue._bootstrap_vue_directives_ = Vue._bootstrap_vue_directives_ || {};
    var loaded = Vue._bootstrap_vue_directives_[name];

    if (!loaded && def && name) {
      Vue._bootstrap_vue_directives_[name] = true;
      Vue.directive(name, def);
    }

    return loaded;
  }
  /**
   * Register a group of directives as being loaded.
   * @param {object} Vue
   * @param {object} Object of directive definitions
   */

  function registerDirectives(Vue, directives) {
    for (var directive in directives) {
      registerDirective(Vue, directive, directives[directive]);
    }
  }
  /**
   * Install plugin if window.Vue available
   * @param {object} Plugin definition
   */

  function vueUse(VuePlugin) {
    if (typeof window !== 'undefined' && window.Vue) {
      window.Vue.use(VuePlugin);
    }
  }

  var components = {
    BAlert: BAlert
  };
  var index = {
    install: function install(Vue) {
      registerComponents(Vue, components);
    }
  };

  /**
   * Aliasing Object[method] allows the minifier to shorten methods to a single character variable,
   * as well as giving BV a chance to inject polyfills.
   * As long as we avoid
   * - import * as Object from "utils/object"
   * all unused exports should be removed by tree-shaking.
   */
  // @link https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign

  /* istanbul ignore if */
  if (typeof Object.assign !== 'function') {
    Object.assign = function (target, varArgs) {
      // .length of function is 2
      if (target == null) {
        // TypeError if undefined or null
        throw new TypeError('Cannot convert undefined or null to object');
      }

      var to = Object(target);

      for (var index = 1; index < arguments.length; index++) {
        var nextSource = arguments[index];

        if (nextSource != null) {
          // Skip over if undefined or null
          for (var nextKey in nextSource) {
            // Avoid bugs when hasOwnProperty is shadowed
            if (Object.prototype.hasOwnProperty.call(nextSource, nextKey)) {
              to[nextKey] = nextSource[nextKey];
            }
          }
        }
      }

      return to;
    };
  } // @link https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is#Polyfill

  /* istanbul ignore if */


  if (!Object.is) {
    Object.is = function (x, y) {
      // SameValue algorithm
      if (x === y) {
        // Steps 1-5, 7-10
        // Steps 6.b-6.e: +0 != -0
        return x !== 0 || 1 / x === 1 / y;
      } else {
        // Step 6.a: NaN == NaN
        // eslint-disable-next-line no-self-compare
        return x !== x && y !== y;
      }
    };
  }

  var assign = Object.assign;
  var keys = Object.keys;
  var defineProperties = Object.defineProperties;
  var defineProperty = Object.defineProperty;
  var create = Object.create;
  function readonlyDescriptor() {
    return {
      enumerable: true,
      configurable: false,
      writable: false
    };
  }

  // Production steps of ECMA-262, Edition 6, 22.1.2.1
  // es6-ified by @alexsasharegan

  /* istanbul ignore if */
  if (!Array.from) {
    Array.from = function () {
      var toStr = Object.prototype.toString;

      var isCallable = function isCallable(fn) {
        return typeof fn === 'function' || toStr.call(fn) === '[object Function]';
      };

      var toInteger = function toInteger(value) {
        var number = Number(value);

        if (isNaN(number)) {
          return 0;
        }

        if (number === 0 || !isFinite(number)) {
          return number;
        }

        return (number > 0 ? 1 : -1) * Math.floor(Math.abs(number));
      };

      var maxSafeInteger = Math.pow(2, 53) - 1;

      var toLength = function toLength(value) {
        return Math.min(Math.max(toInteger(value), 0), maxSafeInteger);
      }; // The length property of the from method is 1.


      return function from(arrayLike
      /*, mapFn, thisArg */
      ) {
        // 1. Let C be the this value.
        var C = this; // 2. Let items be ToObject(arrayLike).

        var items = Object(arrayLike); // 3. ReturnIfAbrupt(items).

        if (arrayLike == null) {
          throw new TypeError('Array.from requires an array-like object - not null or undefined');
        } // 4. If mapfn is undefined, then let mapping be false.


        var mapFn = arguments.length > 1 ? arguments[1] : void undefined;
        var T;

        if (typeof mapFn !== 'undefined') {
          // 5. else
          // 5. a If IsCallable(mapfn) is false, throw a TypeError exception.
          if (!isCallable(mapFn)) {
            throw new TypeError('Array.from: when provided, the second argument must be a function');
          } // 5. b. If thisArg was supplied, let T be thisArg; else let T be undefined.


          if (arguments.length > 2) {
            T = arguments[2];
          }
        } // 10. Let lenValue be Get(items, "length").
        // 11. Let len be ToLength(lenValue).


        var len = toLength(items.length); // 13. If IsConstructor(C) is true, then
        // 13. a. Let A be the result of calling the [[Construct]] internal method
        // of C with an argument list containing the single item len.
        // 14. a. Else, Let A be ArrayCreate(len).

        var A = isCallable(C) ? Object(new C(len)) : new Array(len); // 16. Let k be 0.

        var k = 0; // 17. Repeat, while k < len… (also steps a - h)

        var kValue;

        while (k < len) {
          kValue = items[k];

          if (mapFn) {
            A[k] = typeof T === 'undefined' ? mapFn(kValue, k) : mapFn.call(T, kValue, k);
          } else {
            A[k] = kValue;
          }

          k += 1;
        } // 18. Let putStatus be Put(A, "length", len, true).


        A.length = len; // 20. Return A.

        return A;
      };
    }();
  } // https://tc39.github.io/ecma262/#sec-array.prototype.find
  // Needed for IE support

  /* istanbul ignore if */


  if (!Array.prototype.find) {
    // eslint-disable-next-line no-extend-native
    Object.defineProperty(Array.prototype, 'find', {
      value: function value(predicate) {
        // 1. Let O be ? ToObject(this value).
        if (this == null) {
          throw new TypeError('"this" is null or not defined');
        }

        var o = Object(this); // 2. Let len be ? ToLength(? Get(O, "length")).

        var len = o.length >>> 0; // 3. If IsCallable(predicate) is false, throw a TypeError exception.

        if (typeof predicate !== 'function') {
          throw new TypeError('predicate must be a function');
        } // 4. If thisArg was supplied, let T be thisArg; else let T be undefined.


        var thisArg = arguments[1]; // 5. Let k be 0.

        var k = 0; // 6. Repeat, while k < len

        while (k < len) {
          // a. Let Pk be ! ToString(k).
          // b. Let kValue be ? Get(O, Pk).
          // c. Let testResult be ToBoolean(? Call(predicate, T, « kValue, k, O »)).
          // d. If testResult is true, return kValue.
          var kValue = o[k];

          if (predicate.call(thisArg, kValue, k, o)) {
            return kValue;
          } // e. Increase k by 1.


          k++;
        } // 7. Return undefined.


        return undefined;
      }
    });
  }
  /* istanbul ignore if */


  if (!Array.isArray) {
    Array.isArray = function (arg) {
      return Object.prototype.toString.call(arg) === '[object Array]';
    };
  } // Static


  var from = Array.from;
  var isArray = Array.isArray; // Instance

  var arrayIncludes = function arrayIncludes(array, value) {
    return array.indexOf(value) !== -1;
  };
  function concat() {
    return Array.prototype.concat.apply([], arguments);
  }

  function identity(x) {
    return x;
  }

  /**
   * Given an array of properties or an object of property keys,
   * plucks all the values off the target object.
   * @param {{}|string[]} keysToPluck
   * @param {{}} objToPluck
   * @param {Function} transformFn
   * @return {{}}
   */

  function pluckProps(keysToPluck, objToPluck) {
    var transformFn = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : identity;
    return (isArray(keysToPluck) ? keysToPluck.slice() : keys(keysToPluck)).reduce(function (memo, prop) {
      // eslint-disable-next-line no-sequences
      return memo[transformFn(prop)] = objToPluck[prop], memo;
    }, {});
  }

  /**
   * The Link component is used in many other BV components.
   * As such, sharing its props makes supporting all its features easier.
   * However, some components need to modify the defaults for their own purpose.
   * Prefer sharing a fresh copy of the props to ensure mutations
   * do not affect other component references to the props.
   *
   * https://github.com/vuejs/vue-router/blob/dev/src/components/link.js
   * @return {{}}
   */

  function propsFactory() {
    return {
      href: {
        type: String,
        default: null
      },
      rel: {
        type: String,
        default: null
      },
      target: {
        type: String,
        default: '_self'
      },
      active: {
        type: Boolean,
        default: false
      },
      disabled: {
        type: Boolean,
        default: false
      },
      // router-link specific props
      to: {
        type: [String, Object],
        default: null
      },
      append: {
        type: Boolean,
        default: false
      },
      replace: {
        type: Boolean,
        default: false
      },
      event: {
        type: [String, Array],
        default: 'click'
      },
      activeClass: {
        type: String // default: undefined

      },
      exact: {
        type: Boolean,
        default: false
      },
      exactActiveClass: {
        type: String // default: undefined

      },
      routerTag: {
        type: String,
        default: 'a'
      },
      // nuxt-link specific prop(s)
      noPrefetch: {
        type: Boolean,
        default: false
      }
    };
  }
  function pickLinkProps(propsToPick) {
    var freshLinkProps = propsFactory(); // Normalize everything to array.

    propsToPick = concat(propsToPick);
    return keys(freshLinkProps).reduce(function (memo, prop) {
      if (arrayIncludes(propsToPick, prop)) {
        memo[prop] = freshLinkProps[prop];
      }

      return memo;
    }, {});
  }

  function computeTag(props, parent) {
    return parent.$router && props.to && !props.disabled ? parent.$nuxt ? 'nuxt-link' : 'router-link' : 'a';
  }

  function isRouterLink(tag) {
    return tag !== 'a';
  }

  function computeHref(_ref, tag) {
    var disabled = _ref.disabled,
        href = _ref.href,
        to = _ref.to;

    // We've already checked the parent.$router in computeTag,
    // so isRouterLink(tag) indicates a live router.
    // When deferring to Vue Router's router-link, don't use the href attr at all.
    // We return null, and then remove href from the attributes passed to router-link
    if (isRouterLink(tag)) {
      return null;
    } // If href explicitly provided


    if (href) {
      return href;
    } // Reconstruct `href` when `to` used, but no router


    if (to) {
      // Fallback to `to` prop (if `to` is a string)
      if (typeof to === 'string') {
        return to;
      } // Fallback to `to.path` prop (if `to` is an object)


      if (_typeof(to) === 'object' && typeof to.path === 'string') {
        return to.path;
      }
    } // If nothing is provided use '#' as a fallback


    return '#';
  }

  function computeRel(_ref2) {
    var target = _ref2.target,
        rel = _ref2.rel;

    if (target === '_blank' && rel === null) {
      return 'noopener';
    }

    return rel || null;
  }

  function clickHandlerFactory(_ref3) {
    var disabled = _ref3.disabled,
        tag = _ref3.tag,
        href = _ref3.href,
        suppliedHandler = _ref3.suppliedHandler,
        parent = _ref3.parent;
    return function onClick(e) {
      if (disabled && e instanceof Event) {
        // Stop event from bubbling up.
        e.stopPropagation(); // Kill the event loop attached to this specific EventTarget.

        e.stopImmediatePropagation();
      } else {
        if (isRouterLink(tag) && e.target.__vue__) {
          e.target.__vue__.$emit('click', e);
        }

        if (typeof suppliedHandler === 'function') {
          suppliedHandler.apply(void 0, arguments);
        }

        parent.$root.$emit('clicked::link', e);
      }

      if (!isRouterLink(tag) && href === '#' || disabled) {
        // Stop scroll-to-top behavior or navigation.
        e.preventDefault();
      }
    };
  } // @vue/component


  var BLink = {
    name: 'BLink',
    functional: true,
    props: propsFactory(),
    render: function render(h, _ref4) {
      var props = _ref4.props,
          data = _ref4.data,
          parent = _ref4.parent,
          children = _ref4.children;
      var tag = computeTag(props, parent);
      var rel = computeRel(props);
      var href = computeHref(props, tag);
      var eventType = isRouterLink(tag) ? 'nativeOn' : 'on';
      var suppliedHandler = (data[eventType] || {}).click;
      var handlers = {
        click: clickHandlerFactory({
          tag: tag,
          href: href,
          disabled: props.disabled,
          suppliedHandler: suppliedHandler,
          parent: parent
        })
      };
      var componentData = mergeData(data, {
        class: {
          active: props.active,
          disabled: props.disabled
        },
        attrs: {
          rel: rel,
          target: props.target,
          tabindex: props.disabled ? '-1' : data.attrs ? data.attrs.tabindex : null,
          'aria-disabled': props.disabled ? 'true' : null
        },
        props: _objectSpread({}, props, {
          tag: props.routerTag
        })
      }); // If href attribute exists on router-link (even undefined or null) it fails working on SSR
      // So we explicitly add it here if needed (i.e. if computeHref() is truthy)

      if (href) {
        componentData.attrs.href = href;
      } // We want to overwrite any click handler since our callback
      // will invoke the user supplied handler if !props.disabled


      componentData[eventType] = _objectSpread({}, componentData[eventType] || {}, handlers);
      return h(tag, componentData, children);
    }
  };

  var linkProps = propsFactory();
  delete linkProps.href.default;
  delete linkProps.to.default;
  var props$1 = _objectSpread({}, linkProps, {
    tag: {
      type: String,
      default: 'span'
    },
    variant: {
      type: String,
      default: 'secondary'
    },
    pill: {
      type: Boolean,
      default: false
    } // @vue/component

  });
  var BBadge = {
    name: 'BBadge',
    functional: true,
    props: props$1,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var tag = !props.href && !props.to ? props.tag : BLink;
      var componentData = {
        staticClass: 'badge',
        class: [!props.variant ? 'badge-secondary' : "badge-".concat(props.variant), {
          'badge-pill': Boolean(props.pill),
          active: props.active,
          disabled: props.disabled
        }],
        props: pluckProps(linkProps, props)
      };
      return h(tag, mergeData(data, componentData), children);
    }
  };

  var components$1 = {
    BBadge: BBadge
  };
  var index$1 = {
    install: function install(Vue) {
      registerComponents(Vue, components$1);
    }
  };

  var stripTagsRegex = /(<([^>]+)>)/gi;
  function stripTags() {
    var text = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
    return text.replace(stripTagsRegex, '');
  }
  function htmlOrText(innerHTML, textContent) {
    return innerHTML ? {
      innerHTML: innerHTML
    } : {
      textContent: textContent
    };
  }

  var props$2 = _objectSpread({}, propsFactory(), {
    text: {
      type: String,
      default: null
    },
    html: {
      type: String,
      default: null
    },
    ariaCurrent: {
      type: String,
      default: 'location'
    } // @vue/component

  });
  var BBreadcrumbLink = {
    name: 'BBreadcrumbLink',
    functional: true,
    props: props$2,
    render: function render(h, _ref) {
      var suppliedProps = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var tag = suppliedProps.active ? 'span' : BLink;
      var componentData = {
        props: pluckProps(props$2, suppliedProps)
      };

      if (suppliedProps.active) {
        componentData.attrs = {
          'aria-current': suppliedProps.ariaCurrent
        };
      }

      if (!children) {
        componentData.domProps = htmlOrText(suppliedProps.html, suppliedProps.text);
      }

      return h(tag, mergeData(data, componentData), children);
    }
  };

  var BBreadcrumbItem = {
    name: 'BBreadcrumbItem',
    functional: true,
    props: props$2,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h('li', mergeData(data, {
        staticClass: 'breadcrumb-item',
        class: {
          active: props.active
        },
        attrs: {
          role: 'presentation'
        }
      }), [h(BBreadcrumbLink, {
        props: props
      }, children)]);
    }
  };

  var props$3 = {
    items: {
      type: Array,
      default: null
    } // @vue/component

  };
  var BBreadcrumb = {
    name: 'BBreadcrumb',
    functional: true,
    props: props$3,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var childNodes = children; // Build child nodes from items if given.

      if (isArray(props.items)) {
        var activeDefined = false;
        childNodes = props.items.map(function (item, idx) {
          if (_typeof(item) !== 'object') {
            item = {
              text: item
            };
          } // Copy the value here so we can normalize it.


          var active = item.active;

          if (active) {
            activeDefined = true;
          }

          if (!active && !activeDefined) {
            // Auto-detect active by position in list.
            active = idx + 1 === props.items.length;
          }

          return h(BBreadcrumbItem, {
            props: _objectSpread({}, item, {
              active: active
            })
          });
        });
      }

      return h('ol', mergeData(data, {
        staticClass: 'breadcrumb'
      }), childNodes);
    }
  };

  var components$2 = {
    BBreadcrumb: BBreadcrumb,
    BBreadcrumbItem: BBreadcrumbItem,
    BBreadcrumbLink: BBreadcrumbLink
  };
  var index$2 = {
    install: function install(Vue) {
      registerComponents(Vue, components$2);
    }
  };

  // Info about the current environment
  var inBrowser = typeof document !== 'undefined' && typeof window !== 'undefined';
  var isServer = !inBrowser;
  var hasTouchSupport = inBrowser && ('ontouchstart' in document.documentElement || navigator.maxTouchPoints > 0);
  var hasPointerEvent = inBrowser && Boolean(window.PointerEvent || window.MSPointerEvent);

  var passiveEventSupported = false;
  /* istanbul ignore if */

  if (inBrowser) {
    try {
      var options = {
        get passive() {
          // This function will be called when the browser
          // attempts to access the passive property.
          passiveEventSupported = true;
        }

      };
      window.addEventListener('test', options, options);
      window.removeEventListener('test', options, options);
    } catch (err) {
      passiveEventSupported = false;
    }
  } // Normalize event options based on support of passive option


  function parseEventOptions(options) {
    var useCapture = false;

    if (options) {
      if (_typeof(options) === 'object') {
        // eslint-disable-next-line no-unneeded-ternary
        useCapture = options.useCapture ? true : false;
      } else {
        useCapture = options;
      }
    }

    return passiveEventSupported ? options : useCapture;
  } // Attach an event listener to an element


  var eventOn = function eventOn(el, evtName, handler, options) {
    if (el && el.addEventListener) {
      el.addEventListener(evtName, handler, parseEventOptions(options));
    }
  }; // Remove an event listener from an element

  var eventOff = function eventOff(el, evtName, handler, options) {
    if (el && el.removeEventListener) {
      el.removeEventListener(evtName, handler, parseEventOptions(options));
    }
  }; // Determine if an element is an HTML Element

  var isElement = function isElement(el) {
    return el && el.nodeType === Node.ELEMENT_NODE;
  }; // Determine if an HTML element is visible - Faster than CSS check

  var isVisible = function isVisible(el) {
    /* istanbul ignore next: getBoundingClientRect not avaiable in JSDOM */
    return isElement(el) && document.body.contains(el) && el.getBoundingClientRect().height > 0 && el.getBoundingClientRect().width > 0;
  }; // Determine if an element is disabled

  var isDisabled = function isDisabled(el) {
    return !isElement(el) || el.disabled || el.classList.contains('disabled') || Boolean(el.getAttribute('disabled'));
  }; // Cause/wait-for an element to reflow it's content (adjusting it's height/width)

  var reflow = function reflow(el) {
    // requsting an elements offsetHight will trigger a reflow of the element content

    /* istanbul ignore next: reflow doesnt happen in JSDOM */
    return isElement(el) && el.offsetHeight;
  }; // Select all elements matching selector. Returns [] if none found

  var selectAll = function selectAll(selector, root) {
    if (!isElement(root)) {
      root = document;
    }

    return from(root.querySelectorAll(selector));
  }; // Select a single element, returns null if not found

  var select = function select(selector, root) {
    if (!isElement(root)) {
      root = document;
    }

    return root.querySelector(selector) || null;
  }; // Determine if an element matches a selector

  var matches = function matches(el, selector) {
    if (!isElement(el)) {
      return false;
    } // https://developer.mozilla.org/en-US/docs/Web/API/Element/matches#Polyfill
    // Prefer native implementations over polyfill function


    var proto = Element.prototype;
    /* istanbul ignore next */

    var Matches = proto.matches || proto.matchesSelector || proto.mozMatchesSelector || proto.msMatchesSelector || proto.oMatchesSelector || proto.webkitMatchesSelector || function (sel)
    /* istanbul ignore next */
    {
      var element = this;
      var m = selectAll(sel, element.document || element.ownerDocument);
      var i = m.length; // eslint-disable-next-line no-empty

      while (--i >= 0 && m.item(i) !== element) {}

      return i > -1;
    };

    return Matches.call(el, selector);
  }; // Finds closest element matching selector. Returns null if not found

  var closest = function closest(selector, root) {
    if (!isElement(root)) {
      return null;
    } // https://developer.mozilla.org/en-US/docs/Web/API/Element/closest
    // Since we dont support IE < 10, we can use the "Matches" version of the polyfill for speed
    // Prefer native implementation over polyfill function

    /* istanbul ignore next */


    var Closest = Element.prototype.closest || function (sel) {
      var element = this;

      if (!document.documentElement.contains(element)) {
        return null;
      }

      do {
        // Use our "patched" matches function
        if (matches(element, sel)) {
          return element;
        }

        element = element.parentElement;
      } while (element !== null);

      return null;
    };

    var el = Closest.call(root, selector); // Emulate jQuery closest and return null if match is the passed in element (root)

    return el === root ? null : el;
  }; // Returns true if the parent element contains the child element

  var contains = function contains(parent, child) {
    if (!parent || typeof parent.contains !== 'function') {
      return false;
    }

    return parent.contains(child);
  }; // Get an element given an ID

  var getById = function getById(id) {
    return document.getElementById(/^#/.test(id) ? id.slice(1) : id) || null;
  }; // Add a class to an element

  var addClass = function addClass(el, className) {
    if (className && isElement(el)) {
      el.classList.add(className);
    }
  }; // Remove a class from an element

  var removeClass = function removeClass(el, className) {
    if (className && isElement(el)) {
      el.classList.remove(className);
    }
  }; // Test if an element has a class

  var hasClass = function hasClass(el, className) {
    if (className && isElement(el)) {
      return el.classList.contains(className);
    }

    return false;
  }; // Set an attribute on an element

  var setAttr = function setAttr(el, attr, value) {
    if (attr && isElement(el)) {
      el.setAttribute(attr, value);
    }
  }; // Remove an attribute from an element

  var removeAttr = function removeAttr(el, attr) {
    if (attr && isElement(el)) {
      el.removeAttribute(attr);
    }
  }; // Get an attribute value from an element (returns null if not found)

  var getAttr = function getAttr(el, attr) {
    if (attr && isElement(el)) {
      return el.getAttribute(attr);
    }

    return null;
  }; // Determine if an attribute exists on an element (returns true or false, or null if element not found)

  var hasAttr = function hasAttr(el, attr) {
    if (attr && isElement(el)) {
      return el.hasAttribute(attr);
    }

    return null;
  }; // Return the Bounding Client Rec of an element. Retruns null if not an element

  /* istanbul ignore next: getBoundingClientRect() doesnt work in JSDOM */

  var getBCR = function getBCR(el) {
    return isElement(el) ? el.getBoundingClientRect() : null;
  }; // Get computed style object for an element

  /* istanbul ignore next: getComputedStyle() doesnt work in JSDOM */

  var getCS = function getCS(el) {
    return isElement(el) ? window.getComputedStyle(el) : {};
  }; // Return an element's offset wrt document element
  // https://j11y.io/jquery/#v=git&fn=jQuery.fn.offset

  /* istanbul ignore next: getBoundingClientRect(), getClientRects() doesnt work in JSDOM */

  var offset = function offset(el) {
    if (isElement(el)) {
      if (!el.getClientRects().length) {
        return {
          top: 0,
          left: 0
        };
      }

      var bcr = getBCR(el);
      var win = el.ownerDocument.defaultView;
      return {
        top: bcr.top + win.pageYOffset,
        left: bcr.left + win.pageXOffset
      };
    }
  }; // Return an element's offset wrt to it's offsetParent
  // https://j11y.io/jquery/#v=git&fn=jQuery.fn.position

  /* istanbul ignore next: getBoundingClientRect(), getClientRects() doesnt work in JSDOM */

  var position = function position(el) {
    if (!isElement(el)) {
      return;
    }

    var parentOffset = {
      top: 0,
      left: 0
    };
    var offsetSelf;
    var offsetParent;

    if (getCS(el).position === 'fixed') {
      offsetSelf = getBCR(el);
    } else {
      offsetSelf = offset(el);
      var doc = el.ownerDocument;
      offsetParent = el.offsetParent || doc.documentElement;

      while (offsetParent && (offsetParent === doc.body || offsetParent === doc.documentElement) && getCS(offsetParent).position === 'static') {
        offsetParent = offsetParent.parentNode;
      }

      if (offsetParent && offsetParent !== el && offsetParent.nodeType === Node.ELEMENT_NODE) {
        parentOffset = offset(offsetParent);
        parentOffset.top += parseFloat(getCS(offsetParent).borderTopWidth);
        parentOffset.left += parseFloat(getCS(offsetParent).borderLeftWidth);
      }
    }

    return {
      top: offsetSelf.top - parentOffset.top - parseFloat(getCS(el).marginTop),
      left: offsetSelf.left - parentOffset.left - parseFloat(getCS(el).marginLeft)
    };
  };

  var btnProps = {
    block: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: null
    },
    variant: {
      type: String,
      default: null
    },
    type: {
      type: String,
      default: 'button'
    },
    tag: {
      type: String,
      default: 'button'
    },
    pressed: {
      // tri-state prop: true, false or null
      // => on, off, not a toggle
      type: Boolean,
      default: null
    }
  };
  var linkProps$1 = propsFactory();
  delete linkProps$1.href.default;
  delete linkProps$1.to.default;
  var linkPropKeys = keys(linkProps$1);
  var props$4 = _objectSpread({}, linkProps$1, btnProps); // Focus handler for toggle buttons.  Needs class of 'focus' when focused.

  function handleFocus(evt) {
    if (evt.type === 'focusin') {
      addClass(evt.target, 'focus');
    } else if (evt.type === 'focusout') {
      removeClass(evt.target, 'focus');
    }
  } // Helper functons to minimize runtime memory footprint when lots of buttons on page
  // Is the requested button a link?


  function isLink(props) {
    // If tag prop is set to `a`, we use a b-link to get proper disabled handling
    return Boolean(props.href || props.to || props.tag && String(props.tag).toLowerCase() === 'a');
  } // Is the button to be a toggle button?


  function isToggle(props) {
    return typeof props.pressed === 'boolean';
  } // Is the button "really" a button?


  function isButton(props) {
    if (isLink(props)) {
      return false;
    } else if (props.tag && String(props.tag).toLowerCase() !== 'button') {
      return false;
    }

    return true;
  } // Is the requested tag not a button or link?


  function isNonStandardTag(props) {
    return !isLink(props) && !isButton(props);
  } // Compute required classes (non static classes)


  function computeClass(props) {
    var _ref;

    return [props.variant ? "btn-".concat(props.variant) : "btn-secondary", (_ref = {}, _defineProperty(_ref, "btn-".concat(props.size), Boolean(props.size)), _defineProperty(_ref, 'btn-block', props.block), _defineProperty(_ref, "disabled", props.disabled), _defineProperty(_ref, "active", props.pressed), _ref)];
  } // Compute the link props to pass to b-link (if required)


  function computeLinkProps(props) {
    return isLink(props) ? pluckProps(linkPropKeys, props) : null;
  } // Compute the attributes for a button


  function computeAttrs(props, data) {
    var button = isButton(props);
    var link = isLink(props);
    var toggle = isToggle(props);
    var nonStdTag = isNonStandardTag(props);
    var role = data.attrs && data.attrs['role'] ? data.attrs['role'] : null;
    var tabindex = data.attrs ? data.attrs['tabindex'] : null;

    if (nonStdTag) {
      tabindex = '0';
    }

    return {
      // Type only used for "real" buttons
      type: button && !link ? props.type : null,
      // Disabled only set on "real" buttons
      disabled: button ? props.disabled : null,
      // We add a role of button when the tag is not a link or button for ARIA.
      // Don't bork any role provided in data.attrs when isLink or isButton
      role: nonStdTag ? 'button' : role,
      // We set the aria-disabled state for non-standard tags
      'aria-disabled': nonStdTag ? String(props.disabled) : null,
      // For toggles, we need to set the pressed state for ARIA
      'aria-pressed': toggle ? String(props.pressed) : null,
      // autocomplete off is needed in toggle mode to prevent some browsers from
      // remembering the previous setting when using the back button.
      autocomplete: toggle ? 'off' : null,
      // Tab index is used when the component is not a button.
      // Links are tabbable, but don't allow disabled, while non buttons or links
      // are not tabbable, so we mimic that functionality by disabling tabbing
      // when disabled, and adding a tabindex of '0' to non buttons or non links.
      tabindex: props.disabled && !button ? '-1' : tabindex
    };
  } // @vue/component


  var BButton = {
    name: 'BButton',
    functional: true,
    props: props$4,
    render: function render(h, _ref2) {
      var props = _ref2.props,
          data = _ref2.data,
          listeners = _ref2.listeners,
          children = _ref2.children;
      var toggle = isToggle(props);
      var link = isLink(props);
      var on = {
        click: function click(e) {
          if (props.disabled && e instanceof Event) {
            e.stopPropagation();
            e.preventDefault();
          } else if (toggle && listeners && listeners['update:pressed']) {
            // Send .sync updates to any "pressed" prop (if .sync listeners)
            // Concat will normalize the value to an array
            // without double wrapping an array value in an array.
            concat(listeners['update:pressed']).forEach(function (fn) {
              if (typeof fn === 'function') {
                fn(!props.pressed);
              }
            });
          }
        }
      };

      if (toggle) {
        on.focusin = handleFocus;
        on.focusout = handleFocus;
      }

      var componentData = {
        staticClass: 'btn',
        class: computeClass(props),
        props: computeLinkProps(props),
        attrs: computeAttrs(props, data),
        on: on
      };
      return h(link ? BLink : props.tag, mergeData(data, componentData), children);
    }
  };

  var components$3 = {
    BButton: BButton,
    BBtn: BButton,
    BButtonClose: BButtonClose,
    BBtnClose: BButtonClose
  };
  var index$3 = {
    install: function install(Vue) {
      registerComponents(Vue, components$3);
    }
  };

  var props$5 = {
    vertical: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: null
    },
    tag: {
      type: String,
      default: 'div'
    },
    ariaRole: {
      type: String,
      default: 'group'
    } // @vue/component

  };
  var BButtonGroup = {
    name: 'BButtonGroup',
    functional: true,
    props: props$5,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        class: _defineProperty({
          'btn-group': !props.vertical,
          'btn-group-vertical': props.vertical
        }, "btn-group-".concat(props.size), Boolean(props.size)),
        attrs: {
          role: props.ariaRole
        }
      }), children);
    }
  };

  var components$4 = {
    BButtonGroup: BButtonGroup,
    BBtnGroup: BButtonGroup
  };
  var index$4 = {
    install: function install(Vue) {
      registerComponents(Vue, components$4);
    }
  };

  /*
   * Key Codes (events)
   */
  var KeyCodes = {
    SPACE: 32,
    ENTER: 13,
    ESC: 27,
    LEFT: 37,
    UP: 38,
    RIGHT: 39,
    DOWN: 40,
    PAGEUP: 33,
    PAGEDOWN: 34,
    HOME: 36,
    END: 35,
    TAB: 9,
    SHIFT: 16,
    CTRL: 17,
    BACKSPACE: 8,
    ALT: 18,
    PAUSE: 19,
    BREAK: 19,
    INSERT: 45,
    INS: 45,
    DELETE: 46
  };

  var ITEM_SELECTOR = ['.btn:not(.disabled):not([disabled]):not(.dropdown-item)', '.form-control:not(.disabled):not([disabled])', 'select:not(.disabled):not([disabled])', 'input[type="checkbox"]:not(.disabled)', 'input[type="radio"]:not(.disabled)'].join(','); // @vue/component

  var BButtonToolbar = {
    name: 'BButtonToolbar',
    props: {
      justify: {
        type: Boolean,
        default: false
      },
      keyNav: {
        type: Boolean,
        default: false
      }
    },
    computed: {
      classObject: function classObject() {
        return ['btn-toolbar', this.justify && !this.vertical ? 'justify-content-between' : ''];
      }
    },
    mounted: function mounted() {
      if (this.keyNav) {
        // Pre-set the tabindexes if the markup does not include tabindex="-1" on the toolbar items
        this.getItems();
      }
    },
    methods: {
      onFocusin: function onFocusin(evt) {
        if (evt.target === this.$el) {
          evt.preventDefault();
          evt.stopPropagation();
          this.focusFirst(evt);
        }
      },
      onKeydown: function onKeydown(evt) {
        if (!this.keyNav) {
          return;
        }

        var key = evt.keyCode;
        var shift = evt.shiftKey;

        if (key === KeyCodes.UP || key === KeyCodes.LEFT) {
          evt.preventDefault();
          evt.stopPropagation();

          if (shift) {
            this.focusFirst(evt);
          } else {
            this.focusNext(evt, true);
          }
        } else if (key === KeyCodes.DOWN || key === KeyCodes.RIGHT) {
          evt.preventDefault();
          evt.stopPropagation();

          if (shift) {
            this.focusLast(evt);
          } else {
            this.focusNext(evt, false);
          }
        }
      },
      setItemFocus: function setItemFocus(item) {
        this.$nextTick(function () {
          item.focus();
        });
      },
      focusNext: function focusNext(evt, prev) {
        var items = this.getItems();

        if (items.length < 1) {
          return;
        }

        var index = items.indexOf(evt.target);

        if (prev && index > 0) {
          index--;
        } else if (!prev && index < items.length - 1) {
          index++;
        }

        if (index < 0) {
          index = 0;
        }

        this.setItemFocus(items[index]);
      },
      focusFirst: function focusFirst(evt) {
        var items = this.getItems();

        if (items.length > 0) {
          this.setItemFocus(items[0]);
        }
      },
      focusLast: function focusLast(evt) {
        var items = this.getItems();

        if (items.length > 0) {
          this.setItemFocus([items.length - 1]);
        }
      },
      getItems: function getItems() {
        var items = selectAll(ITEM_SELECTOR, this.$el);
        items.forEach(function (item) {
          // Ensure tabfocus is -1 on any new elements
          item.tabIndex = -1;
        });
        return items.filter(function (el) {
          return isVisible(el);
        });
      }
    },
    render: function render(h) {
      return h('div', {
        class: this.classObject,
        attrs: {
          role: 'toolbar',
          tabindex: this.keyNav ? '0' : null
        },
        on: {
          focusin: this.onFocusin,
          keydown: this.onKeydown
        }
      }, [this.$slots.default]);
    }
  };

  var components$5 = {
    BButtonToolbar: BButtonToolbar,
    BBtnToolbar: BButtonToolbar
  };
  var index$5 = {
    install: function install(Vue) {
      registerComponents(Vue, components$5);
    }
  };

  var props$6 = {
    tag: {
      type: String,
      default: 'div'
    } // @vue/component

  };
  var InputGroupText = {
    name: 'BInputGroupText',
    functional: true,
    props: props$6,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        staticClass: 'input-group-text'
      }), children);
    }
  };

  var commonProps = {
    id: {
      type: String,
      default: null
    },
    tag: {
      type: String,
      default: 'div'
    },
    isText: {
      type: Boolean,
      default: false
    } // @vue/component

  };
  var InputGroupAddon = {
    name: 'BInputGroupAddon',
    functional: true,
    props: _objectSpread({}, commonProps, {
      append: {
        type: Boolean,
        default: false
      }
    }),
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        class: {
          'input-group-append': props.append,
          'input-group-prepend': !props.append
        },
        attrs: {
          id: props.id
        }
      }), props.isText ? [h(InputGroupText, children)] : children);
    }
  };

  var InputGroupPrepend = {
    name: 'BInputGroupPrepend',
    functional: true,
    props: commonProps,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      // pass all our props/attrs down to child, and set`append` to false
      return h(InputGroupAddon, mergeData(data, {
        props: _objectSpread({}, props, {
          append: false
        })
      }), children);
    }
  };

  var InputGroupAppend = {
    name: 'BInputGroupAppend',
    functional: true,
    props: commonProps,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      // pass all our props/attrs down to child, and set`append` to true
      return h(InputGroupAddon, mergeData(data, {
        props: _objectSpread({}, props, {
          append: true
        })
      }), children);
    }
  };

  var props$7 = {
    id: {
      type: String
    },
    size: {
      type: String
    },
    prepend: {
      type: String
    },
    prependHTML: {
      type: String
    },
    append: {
      type: String
    },
    appendHTML: {
      type: String
    },
    tag: {
      type: String,
      default: 'div'
    } // @vue/component

  };
  var BInputGroup = {
    name: 'BInputGroup',
    functional: true,
    props: props$7,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          slots = _ref.slots;
      var $slots = slots();
      var childNodes = []; // Prepend prop

      if (props.prepend) {
        childNodes.push(h(InputGroupPrepend, [h(InputGroupText, {
          domProps: htmlOrText(props.prependHTML, props.prepend)
        })]));
      } else {
        childNodes.push(h(false));
      } // Prepend slot


      if ($slots.prepend) {
        childNodes.push(h(InputGroupPrepend, $slots.prepend));
      } else {
        childNodes.push(h(false));
      } // Default slot


      if ($slots.default) {
        childNodes.push.apply(childNodes, _toConsumableArray($slots.default));
      } else {
        childNodes.push(h(false));
      } // Append prop


      if (props.append) {
        childNodes.push(h(InputGroupAppend, [h(InputGroupText, {
          domProps: htmlOrText(props.appendHTML, props.append)
        })]));
      } else {
        childNodes.push(h(false));
      } // Append slot


      if ($slots.append) {
        childNodes.push(h(InputGroupAppend, $slots.append));
      } else {
        childNodes.push(h(false));
      }

      return h(props.tag, mergeData(data, {
        staticClass: 'input-group',
        class: _defineProperty({}, "input-group-".concat(props.size), Boolean(props.size)),
        attrs: {
          id: props.id || null,
          role: 'group'
        }
      }), childNodes);
    }
  };

  var components$6 = {
    BInputGroup: BInputGroup,
    BInputGroupAddon: InputGroupAddon,
    BInputGroupPrepend: InputGroupPrepend,
    BInputGroupAppend: InputGroupAppend,
    BInputGroupText: InputGroupText
  };
  var index$6 = {
    install: function install(Vue) {
      registerComponents(Vue, components$6);
    }
  };

  /**
   * @param {string} str
   */
  function upperFirst(str) {
    if (typeof str !== 'string') {
      str = String(str);
    }

    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  /**
   * @param {string} prefix
   * @param {string} value
   */

  function prefixPropName(prefix, value) {
    return prefix + upperFirst(value);
  }

  /**
   * @param {string} str
   */
  function lowerFirst(str) {
    if (typeof str !== 'string') {
      str = String(str);
    }

    return str.charAt(0).toLowerCase() + str.slice(1);
  }

  /**
   * @param {string} prefix
   * @param {string} value
   */

  function unPrefixPropName(prefix, value) {
    return lowerFirst(value.replace(prefix, ''));
  }

  /**
   * @param {[]|{}} props
   * @param {Function} transformFn
   */

  function copyProps(props) {
    var transformFn = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : identity;

    if (isArray(props)) {
      return props.map(transformFn);
    } // Props as an object.


    var copied = {};

    for (var prop in props) {
      if (props.hasOwnProperty(prop)) {
        if (_typeof(prop) === 'object') {
          copied[transformFn(prop)] = _objectSpread({}, props[prop]);
        } else {
          copied[transformFn(prop)] = props[prop];
        }
      }
    }

    return copied;
  }

  // @vue/component
  var cardMixin = {
    props: {
      tag: {
        type: String,
        default: 'div'
      },
      bgVariant: {
        type: String,
        default: null
      },
      borderVariant: {
        type: String,
        default: null
      },
      textVariant: {
        type: String,
        default: null
      }
    }
  };

  var props$8 = {
    title: {
      type: String,
      default: ''
    },
    titleTag: {
      type: String,
      default: 'h4'
    } // @vue/component

  };
  var BCardTitle = {
    name: 'BCardTitle',
    functional: true,
    props: props$8,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.titleTag, mergeData(data, {
        staticClass: 'card-title'
      }), children || props.title);
    }
  };

  var props$9 = {
    subTitle: {
      type: String,
      default: ''
    },
    subTitleTag: {
      type: String,
      default: 'h6'
    },
    subTitleTextVariant: {
      type: String,
      default: 'muted'
    } // @vue/component

  };
  var BCardSubTitle = {
    name: 'BCardSubTitle',
    functional: true,
    props: props$9,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.subTitleTag, mergeData(data, {
        staticClass: 'card-subtitle',
        class: [props.subTitleTextVariant ? "text-".concat(props.subTitleTextVariant) : null]
      }), children || props.subTitle);
    }
  };

  var props$a = _objectSpread({}, copyProps(cardMixin.props, prefixPropName.bind(null, 'body')), {
    bodyClass: {
      type: [String, Object, Array],
      default: null
    }
  }, props$8, props$9, {
    overlay: {
      type: Boolean,
      default: false
    } // @vue/component

  });
  var BCardBody = {
    name: 'BCardBody',
    functional: true,
    props: props$a,
    render: function render(h, _ref) {
      var _ref2;

      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var cardTitle = h(false);
      var cardSubTitle = h(false);
      var cardContent = children || [h(false)];

      if (props.title) {
        cardTitle = h(BCardTitle, {
          props: pluckProps(props$8, props)
        });
      }

      if (props.subTitle) {
        cardSubTitle = h(BCardSubTitle, {
          props: pluckProps(props$9, props),
          class: ['mb-2']
        });
      }

      return h(props.bodyTag, mergeData(data, {
        staticClass: 'card-body',
        class: [(_ref2 = {
          'card-img-overlay': props.overlay
        }, _defineProperty(_ref2, "bg-".concat(props.bodyBgVariant), Boolean(props.bodyBgVariant)), _defineProperty(_ref2, "border-".concat(props.bodyBorderVariant), Boolean(props.bodyBorderVariant)), _defineProperty(_ref2, "text-".concat(props.bodyTextVariant), Boolean(props.bodyTextVariant)), _ref2), props.bodyClass || {}]
      }), [cardTitle, cardSubTitle].concat(_toConsumableArray(cardContent)));
    }
  };

  var props$b = _objectSpread({}, copyProps(cardMixin.props, prefixPropName.bind(null, 'header')), {
    header: {
      type: String,
      default: null
    },
    headerHtml: {
      type: String,
      default: null
    },
    headerClass: {
      type: [String, Object, Array],
      default: null
    } // @vue/component

  });
  var BCardHeader = {
    name: 'BCardHeader',
    functional: true,
    props: props$b,
    render: function render(h, _ref) {
      var _ref2;

      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.headerTag, mergeData(data, {
        staticClass: 'card-header',
        class: [props.headerClass, (_ref2 = {}, _defineProperty(_ref2, "bg-".concat(props.headerBgVariant), Boolean(props.headerBgVariant)), _defineProperty(_ref2, "border-".concat(props.headerBorderVariant), Boolean(props.headerBorderVariant)), _defineProperty(_ref2, "text-".concat(props.headerTextVariant), Boolean(props.headerTextVariant)), _ref2)]
      }), children || [h('div', {
        domProps: htmlOrText(props.headerHtml, props.header)
      })]);
    }
  };

  var props$c = _objectSpread({}, copyProps(cardMixin.props, prefixPropName.bind(null, 'footer')), {
    footer: {
      type: String,
      default: null
    },
    footerHtml: {
      type: String,
      default: null
    },
    footerClass: {
      type: [String, Object, Array],
      default: null
    } // @vue/component

  });
  var BCardFooter = {
    name: 'BCardFooter',
    functional: true,
    props: props$c,
    render: function render(h, _ref) {
      var _ref2;

      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.footerTag, mergeData(data, {
        staticClass: 'card-footer',
        class: [props.footerClass, (_ref2 = {}, _defineProperty(_ref2, "bg-".concat(props.footerBgVariant), Boolean(props.footerBgVariant)), _defineProperty(_ref2, "border-".concat(props.footerBorderVariant), Boolean(props.footerBorderVariant)), _defineProperty(_ref2, "text-".concat(props.footerTextVariant), Boolean(props.footerTextVariant)), _ref2)]
      }), children || [h('div', {
        domProps: htmlOrText(props.footerHtml, props.footer)
      })]);
    }
  };

  var props$d = {
    src: {
      type: String,
      default: null,
      required: true
    },
    alt: {
      type: String,
      default: null
    },
    top: {
      type: Boolean,
      default: false
    },
    bottom: {
      type: Boolean,
      default: false
    },
    left: {
      type: Boolean,
      default: false
    },
    start: {
      type: Boolean,
      default: false // alias of 'left'

    },
    right: {
      type: Boolean,
      default: false
    },
    end: {
      type: Boolean,
      default: false // alias of 'right'

    },
    height: {
      type: String,
      default: null
    },
    width: {
      type: String,
      default: null
    } // @vue/component

  };
  var BCardImg = {
    name: 'BCardImg',
    functional: true,
    props: props$d,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data;
      var baseClass = 'card-img';

      if (props.top) {
        baseClass += '-top';
      } else if (props.right || props.end) {
        baseClass += '-right';
      } else if (props.bottom) {
        baseClass += '-bottom';
      } else if (props.left || props.start) {
        baseClass += '-left';
      }

      return h('img', mergeData(data, {
        class: [baseClass],
        attrs: {
          src: props.src,
          alt: props.alt,
          height: props.height,
          width: props.width
        }
      }));
    }
  };

  var cardImgProps = copyProps(props$d, prefixPropName.bind(null, 'img'));
  cardImgProps.imgSrc.required = false;
  var props$e = _objectSpread({}, props$a, props$b, props$c, cardImgProps, copyProps(cardMixin.props), {
    align: {
      type: String,
      default: null
    },
    noBody: {
      type: Boolean,
      default: false
    } // @vue/component

  });
  var BCard = {
    name: 'BCard',
    functional: true,
    props: props$e,
    render: function render(h, _ref) {
      var _class;

      var props = _ref.props,
          data = _ref.data,
          slots = _ref.slots;
      var $slots = slots(); // Create placeholder elements for each section

      var imgFirst = h(false);
      var header = h(false);
      var content = h(false);
      var footer = h(false);
      var imgLast = h(false);

      if (props.imgSrc) {
        var img = h(BCardImg, {
          props: pluckProps(cardImgProps, props, unPrefixPropName.bind(null, 'img'))
        });

        if (props.imgBottom) {
          imgLast = img;
        } else {
          imgFirst = img;
        }
      }

      if (props.header || $slots.header) {
        header = h(BCardHeader, {
          props: pluckProps(props$b, props)
        }, $slots.header);
      }

      if (props.noBody) {
        content = $slots.default || [];
      } else {
        // Wrap content in card-body
        content = [h(BCardBody, {
          props: pluckProps(props$a, props)
        }, $slots.default)];
      }

      if (props.footer || $slots.footer) {
        footer = h(BCardFooter, {
          props: pluckProps(props$c, props)
        }, $slots.footer);
      }

      return h(props.tag, mergeData(data, {
        staticClass: 'card',
        class: (_class = {
          'flex-row': props.imgLeft || props.imgStart,
          'flex-row-reverse': (props.imgRight || props.imgEnd) && !(props.imgLeft || props.imgStart)
        }, _defineProperty(_class, "text-".concat(props.align), Boolean(props.align)), _defineProperty(_class, "bg-".concat(props.bgVariant), Boolean(props.bgVariant)), _defineProperty(_class, "border-".concat(props.borderVariant), Boolean(props.borderVariant)), _defineProperty(_class, "text-".concat(props.textVariant), Boolean(props.textVariant)), _class)
      }), [imgFirst, header].concat(_toConsumableArray(content), [footer, imgLast]));
    }
  };

  var props$f = {
    textTag: {
      type: String,
      default: 'p'
    } // @vue/component

  };
  var BCardText = {
    name: 'BCardText',
    functional: true,
    props: props$f,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.textTag, mergeData(data, {
        staticClass: 'card-text'
      }), children);
    }
  };

  var props$g = {
    tag: {
      type: String,
      default: 'div'
    },
    deck: {
      type: Boolean,
      default: false
    },
    columns: {
      type: Boolean,
      default: false
    } // @vue/component

  };
  var BCardGroup = {
    name: 'BCardGroup',
    functional: true,
    props: props$g,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var baseClass = 'card-group';

      if (props.deck) {
        baseClass = 'card-deck';
      } else if (props.columns) {
        baseClass = 'card-columns';
      }

      return h(props.tag, mergeData(data, {
        class: baseClass
      }), children);
    }
  };

  var components$7 = {
    BCard: BCard,
    BCardHeader: BCardHeader,
    BCardBody: BCardBody,
    BCardTitle: BCardTitle,
    BCardSubTitle: BCardSubTitle,
    BCardFooter: BCardFooter,
    BCardImg: BCardImg,
    BCardText: BCardText,
    BCardGroup: BCardGroup
  };
  var index$7 = {
    install: function install(Vue) {
      registerComponents(Vue, components$7);
    }
  };

  // Emulate observer disconnect() method so that we can detach the events later

  function fakeObserverFactory(el, callback)
  /* istanbul ignore next: hard to test in JSDOM */
  {
    eventOn(el, 'DOMNodeInserted', callback, false);
    eventOn(el, 'DOMNodeRemoved', callback, false);
    return {
      disconnect: function disconnect() {
        eventOff(el, 'DOMNodeInserted', callback, false);
        eventOff(el, 'DOMNodeRemoved', callback, false);
      }
    };
  }
  /**
   * Observe a DOM element changes, falls back to eventListener mode
   * @param {Element} el The DOM element to observe
   * @param {Function} callback callback to be called on change
   * @param {object} [opts={childList: true, subtree: true}] observe options
   * @see http://stackoverflow.com/questions/3219758
   */


  function observeDOM(el, callback, opts)
  /* istanbul ignore next: difficult to test in JSDOM */
  {
    var MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver;
    var eventListenerSupported = window.addEventListener; // Handle case where we might be passed a vue instance

    el = el ? el.$el || el : null;
    /* istanbul ignore next: dificult to test in JSDOM */

    if (!isElement(el)) {
      // We can't observe somthing that isn't an element
      return null;
    }

    var obs = null;

    if (MutationObserver) {
      // Define a new observer
      obs = new MutationObserver(function (mutations) {
        var changed = false; // A Mutation can contain several change records, so we loop through them to see what has changed.
        // We break out of the loop early if any "significant" change has been detected

        for (var i = 0; i < mutations.length && !changed; i++) {
          // The muttion record
          var mutation = mutations[i]; // Mutation Type

          var type = mutation.type; // DOM Node (could be any DOM Node type - HTMLElement, Text, comment, etc)

          var target = mutation.target;

          if (type === 'characterData' && target.nodeType === Node.TEXT_NODE) {
            // We ignore nodes that are not TEXT (i.e. comments, etc) as they don't change layout
            changed = true;
          } else if (type === 'attributes') {
            changed = true;
          } else if (type === 'childList' && (mutation.addedNodes.length > 0 || mutation.removedNodes.length > 0)) {
            // This includes HTMLElement and Text Nodes being added/removed/re-arranged
            changed = true;
          }
        }

        if (changed) {
          // We only call the callback if a change that could affect layout/size truely happened.
          callback();
        }
      }); // Have the observer observe foo for changes in children, etc

      obs.observe(el, _objectSpread({
        childList: true,
        subtree: true
      }, opts));
    } else if (eventListenerSupported) {
      // Legacy interface. most likely not used in modern browsers
      obs = fakeObserverFactory(el, callback);
    } // We return a reference to the observer so that obs.disconnect() can be called if necessary
    // To reduce overhead when the root element is hiiden


    return obs;
  }

  /*
   * SSR Safe Client Side ID attribute generation
   * id's can only be generated client side, after mount.
   * this._uid is not synched between server and client.
   */
  // @vue/component
  var idMixin = {
    props: {
      id: {
        type: String,
        default: null
      }
    },
    data: function data() {
      return {
        localId_: null
      };
    },
    computed: {
      safeId: function safeId() {
        // Computed property that returns a dynamic function for creating the ID.
        // Reacts to changes in both .id and .localId_ And regens a new function
        var id = this.id || this.localId_; // We return a function that accepts an optional suffix string
        // So this computed prop looks and works like a method!!!

        var fn = function fn(suffix) {
          if (!id) {
            return null;
          }

          suffix = String(suffix || '').replace(/\s+/g, '_');
          return suffix ? id + '_' + suffix : id;
        };

        return fn;
      }
    },
    mounted: function mounted() {
      var _this = this;

      // mounted only occurs client side
      this.$nextTick(function () {
        // Update dom with auto ID after dom loaded to prevent
        // SSR hydration errors.
        _this.localId_ = "__BVID__".concat(_this._uid);
      });
    }
  };

  var DIRECTION = {
    next: {
      dirClass: 'carousel-item-left',
      overlayClass: 'carousel-item-next'
    },
    prev: {
      dirClass: 'carousel-item-right',
      overlayClass: 'carousel-item-prev'
    } // Fallback Transition duration (with a little buffer) in ms

  };
  var TRANS_DURATION = 600 + 50; // Time for mouse compat events to fire after touch

  var TOUCHEVENT_COMPAT_WAIT = 500; // Number of pixels to consider touch move a swipe

  var SWIPE_THRESHOLD = 40; // PointerEvent pointer types

  var PointerType = {
    TOUCH: 'touch',
    PEN: 'pen' // Transition Event names

  };
  var TransitionEndEvents = {
    WebkitTransition: 'webkitTransitionEnd',
    MozTransition: 'transitionend',
    OTransition: 'otransitionend oTransitionEnd',
    transition: 'transitionend'
  };
  var EventOptions = {
    passive: true,
    capture: false // Return the browser specific transitionEnd event name

  };

  function getTransisionEndEvent(el) {
    for (var name in TransitionEndEvents) {
      if (el.style[name] !== undefined) {
        /* istanbul ignore next: JSDOM doesn't support transition events */
        return TransitionEndEvents[name];
      }
    } // fallback


    return null;
  } // @vue/component


  var BCarousel = {
    name: 'BCarousel',
    mixins: [idMixin],
    provide: function provide() {
      return {
        carousel: this
      };
    },
    props: {
      labelPrev: {
        type: String,
        default: 'Previous Slide'
      },
      labelNext: {
        type: String,
        default: 'Next Slide'
      },
      labelGotoSlide: {
        type: String,
        default: 'Goto Slide'
      },
      labelIndicators: {
        type: String,
        default: 'Select a slide to display'
      },
      interval: {
        type: Number,
        default: 5000
      },
      indicators: {
        type: Boolean,
        default: false
      },
      controls: {
        type: Boolean,
        default: false
      },
      noAnimation: {
        // Disable slide/fade animation
        type: Boolean,
        default: false
      },
      fade: {
        // Enable cross-fade animation instead of slide animation
        type: Boolean,
        default: false
      },
      noTouch: {
        // Sniffed by carousel-slide
        type: Boolean,
        default: false
      },
      imgWidth: {
        // Sniffed by carousel-slide
        type: [Number, String] // default: undefined

      },
      imgHeight: {
        // Sniffed by carousel-slide
        type: [Number, String] // default: undefined

      },
      background: {
        type: String // default: undefined

      },
      value: {
        type: Number,
        default: 0
      }
    },
    data: function data() {
      return {
        index: this.value || 0,
        isSliding: false,
        transitionEndEvent: null,
        slides: [],
        direction: null,
        isPaused: false,
        // Touch event handling values
        touchStartX: 0,
        touchDeltaX: 0
      };
    },
    watch: {
      value: function value(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.setSlide(newVal);
        }
      },
      interval: function interval(newVal, oldVal) {
        if (newVal === oldVal) {
          return;
        }

        if (!newVal) {
          // Pausing slide show
          this.pause(false);
        } else {
          // Restarting or Changing interval
          this.pause(true);
          this.start(false);
        }
      },
      isPaused: function isPaused(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.$emit(newVal ? 'paused' : 'unpaused');
        }
      },
      index: function index(to, from) {
        if (to === from || this.isSliding) {
          return;
        }

        this.doSlide(to, from);
      }
    },
    created: function created() {
      // Create private non-reactive props
      this._intervalId = null;
      this._animationTimeout = null;
      this._touchTimeout = null;
    },
    mounted: function mounted() {
      // Cache current browser transitionend event name
      this.transitionEndEvent = getTransisionEndEvent(this.$el) || null; // Get all slides

      this.updateSlides(); // Observe child changes so we can update slide list

      observeDOM(this.$refs.inner, this.updateSlides.bind(this), {
        subtree: false,
        childList: true,
        attributes: true,
        attributeFilter: ['id']
      });
    },
    beforeDestroy: function beforeDestroy()
    /* istanbul ignore next: dificult to test */
    {
      clearTimeout(this._animationTimeout);
      clearTimeout(this._touchTimeout);
      clearInterval(this._intervalId);
      this._intervalId = null;
      this._animationTimeout = null;
      this._touchTimeout = null;
    },
    methods: {
      // Set slide
      setSlide: function setSlide(slide) {
        var _this = this;

        var direction = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;

        // Don't animate when page is not visible

        /* istanbul ignore if: dificult to test */
        if (inBrowser && document.visibilityState && document.hidden) {
          return;
        }

        var len = this.slides.length; // Don't do anything if nothing to slide to

        if (len === 0) {
          return;
        } // Don't change slide while transitioning, wait until transition is done


        if (this.isSliding) {
          // Schedule slide after sliding complete
          this.$once('sliding-end', function () {
            return _this.setSlide(slide, direction);
          });
          return;
        }

        this.direction = direction; // Make sure we have an integer (you never know!)

        slide = Math.floor(slide); // Set new slide index. Wrap around if necessary

        this.index = slide >= len ? 0 : slide >= 0 ? slide : len - 1;
      },
      // Previous slide
      prev: function prev() {
        this.setSlide(this.index - 1, 'prev');
      },
      // Next slide
      next: function next() {
        this.setSlide(this.index + 1, 'next');
      },
      // Pause auto rotation
      pause: function pause(evt) {
        if (!evt) {
          this.isPaused = true;
        }

        if (this._intervalId) {
          clearInterval(this._intervalId);
          this._intervalId = null;
        }
      },
      // Start auto rotate slides
      start: function start(evt) {
        if (!evt) {
          this.isPaused = false;
        }

        if (this._intervalId) {
          clearInterval(this._intervalId);
          this._intervalId = null;
        } // Don't start if no interval, or less than 2 slides


        if (this.interval && this.slides.length > 1) {
          this._intervalId = setInterval(this.next, Math.max(1000, this.interval));
        }
      },
      // Re-Start auto rotate slides when focus/hover leaves the carousel
      restart: function restart(evt) {
        /* istanbul ignore if: dificult to test */
        if (!this.$el.contains(document.activeElement)) {
          this.start();
        }
      },
      doSlide: function doSlide(to, from) {
        var _this2 = this;

        var isCycling = Boolean(this.interval); // Determine sliding direction

        var direction = this.calcDirection(this.direction, from, to);
        var overlayClass = direction.overlayClass;
        var dirClass = direction.dirClass; // Determine current and next slides

        var currentSlide = this.slides[from];
        var nextSlide = this.slides[to]; // Don't do anything if there aren't any slides to slide to

        if (!currentSlide || !nextSlide) {
          return;
        } // Start animating


        this.isSliding = true;

        if (isCycling) {
          this.pause(false);
        }

        this.$emit('sliding-start', to); // Update v-model

        this.$emit('input', this.index);

        if (this.noAnimation) {
          addClass(nextSlide, 'active');
          removeClass(currentSlide, 'active');
          this.isSliding = false; // Notify ourselves that we're done sliding (slid)

          this.$nextTick(function () {
            return _this2.$emit('sliding-end', to);
          });
        } else {
          addClass(nextSlide, overlayClass); // Trigger a reflow of next slide

          reflow(nextSlide);
          addClass(currentSlide, dirClass);
          addClass(nextSlide, dirClass); // Transition End handler

          var called = false;
          /* istanbul ignore next: dificult to test */

          var onceTransEnd = function onceTransEnd(evt) {
            if (called) {
              return;
            }

            called = true;
            /* istanbul ignore if: transition events cant be tested in JSDOM */

            if (_this2.transitionEndEvent) {
              var events = _this2.transitionEndEvent.split(/\s+/);

              events.forEach(function (evt) {
                return eventOff(currentSlide, evt, onceTransEnd, EventOptions);
              });
            }

            _this2._animationTimeout = null;
            removeClass(nextSlide, dirClass);
            removeClass(nextSlide, overlayClass);
            addClass(nextSlide, 'active');
            removeClass(currentSlide, 'active');
            removeClass(currentSlide, dirClass);
            removeClass(currentSlide, overlayClass);
            setAttr(currentSlide, 'aria-current', 'false');
            setAttr(nextSlide, 'aria-current', 'true');
            setAttr(currentSlide, 'aria-hidden', 'true');
            setAttr(nextSlide, 'aria-hidden', 'false');
            _this2.isSliding = false;
            _this2.direction = null; // Notify ourselves that we're done sliding (slid)

            _this2.$nextTick(function () {
              return _this2.$emit('sliding-end', to);
            });
          }; // Set up transitionend handler

          /* istanbul ignore if: transition events cant be tested in JSDOM */


          if (this.transitionEndEvent) {
            var events = this.transitionEndEvent.split(/\s+/);
            events.forEach(function (event) {
              return eventOn(currentSlide, event, onceTransEnd, EventOptions);
            });
          } // Fallback to setTimeout


          this._animationTimeout = setTimeout(onceTransEnd, TRANS_DURATION);
        }

        if (isCycling) {
          this.start(false);
        }
      },
      // Update slide list
      updateSlides: function updateSlides() {
        this.pause(true); // Get all slides as DOM elements

        this.slides = selectAll('.carousel-item', this.$refs.inner);
        var numSlides = this.slides.length; // Keep slide number in range

        var index = Math.max(0, Math.min(Math.floor(this.index), numSlides - 1));
        this.slides.forEach(function (slide, idx) {
          var n = idx + 1;

          if (idx === index) {
            addClass(slide, 'active');
            setAttr(slide, 'aria-current', 'true');
          } else {
            removeClass(slide, 'active');
            setAttr(slide, 'aria-current', 'false');
          }

          setAttr(slide, 'aria-posinset', String(n));
          setAttr(slide, 'aria-setsize', String(numSlides));
        }); // Set slide as active

        this.setSlide(index);
        this.start(this.isPaused);
      },
      calcDirection: function calcDirection() {
        var direction = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : null;
        var curIndex = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;
        var nextIndex = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 0;

        if (!direction) {
          return nextIndex > curIndex ? DIRECTION.next : DIRECTION.prev;
        }

        return DIRECTION[direction];
      },
      handleClick: function handleClick(evt, fn) {
        var keyCode = evt.keyCode;

        if (evt.type === 'click' || keyCode === KeyCodes.SPACE || keyCode === KeyCodes.ENTER) {
          evt.preventDefault();
          evt.stopPropagation();
          fn();
        }
      },
      handleSwipe: function handleSwipe()
      /* istanbul ignore next: JSDOM doesn't support touch events */
      {
        var absDeltax = Math.abs(this.touchDeltaX);

        if (absDeltax <= SWIPE_THRESHOLD) {
          return;
        }

        var direction = absDeltax / this.touchDeltaX;

        if (direction > 0) {
          // swipe left
          this.prev();
        } else if (direction < 0) {
          // swipe right
          this.next();
        }
      },
      touchStart: function touchStart(evt)
      /* istanbul ignore next: JSDOM doesn't support touch events */
      {
        if (hasPointerEvent && PointerType[evt.pointerType.toUpperCase()]) {
          this.touchStartX = evt.clientX;
        } else if (!hasPointerEvent) {
          this.touchStartX = evt.touches[0].clientX;
        }
      },
      touchMove: function touchMove(evt)
      /* istanbul ignore next: JSDOM doesn't support touch events */
      {
        // ensure swiping with one touch and not pinching
        if (evt.touches && evt.originalEvent.touches.length > 1) {
          this.touchDeltaX = 0;
        } else {
          this.touchDeltaX = evt.touches[0].clientX - this.touchStartX;
        }
      },
      touchEnd: function touchEnd(evt)
      /* istanbul ignore next: JSDOM doesn't support touch events */
      {
        if (hasPointerEvent && PointerType[evt.pointerType.toUpperCase()]) {
          this.touchDeltaX = evt.clientX - this.touchStartX;
        }

        this.handleSwipe(); // If it's a touch-enabled device, mouseenter/leave are fired as
        // part of the mouse compatibility events on first tap - the carousel
        // would stop cycling until user tapped out of it;
        // here, we listen for touchend, explicitly pause the carousel
        // (as if it's the second time we tap on it, mouseenter compat event
        // is NOT fired) and after a timeout (to allow for mouse compatibility
        // events to fire) we explicitly restart cycling

        this.pause(false);

        if (this._touchTimeout) {
          clearTimeout(this._touchTimeout);
        }

        this._touchTimeout = setTimeout(this.start, TOUCHEVENT_COMPAT_WAIT + Math.max(1000, this.interval));
      }
    },
    render: function render(h) {
      var _this3 = this;

      // Wrapper for slides
      var inner = h('div', {
        ref: 'inner',
        class: ['carousel-inner'],
        attrs: {
          id: this.safeId('__BV_inner_'),
          role: 'list'
        }
      }, [this.$slots.default]); // Prev and Next Controls

      var controls = h(false);

      if (this.controls) {
        controls = [h('a', {
          class: ['carousel-control-prev'],
          attrs: {
            href: '#',
            role: 'button',
            'aria-controls': this.safeId('__BV_inner_')
          },
          on: {
            click: function click(evt) {
              _this3.handleClick(evt, _this3.prev);
            },
            keydown: function keydown(evt) {
              _this3.handleClick(evt, _this3.prev);
            }
          }
        }, [h('span', {
          class: ['carousel-control-prev-icon'],
          attrs: {
            'aria-hidden': 'true'
          }
        }), h('span', {
          class: ['sr-only']
        }, [this.labelPrev])]), h('a', {
          class: ['carousel-control-next'],
          attrs: {
            href: '#',
            role: 'button',
            'aria-controls': this.safeId('__BV_inner_')
          },
          on: {
            click: function click(evt) {
              _this3.handleClick(evt, _this3.next);
            },
            keydown: function keydown(evt) {
              _this3.handleClick(evt, _this3.next);
            }
          }
        }, [h('span', {
          class: ['carousel-control-next-icon'],
          attrs: {
            'aria-hidden': 'true'
          }
        }), h('span', {
          class: ['sr-only']
        }, [this.labelNext])])];
      } // Indicators


      var indicators = h('ol', {
        class: ['carousel-indicators'],
        directives: [{
          name: 'show',
          rawName: 'v-show',
          value: this.indicators,
          expression: 'indicators'
        }],
        attrs: {
          id: this.safeId('__BV_indicators_'),
          'aria-hidden': this.indicators ? 'false' : 'true',
          'aria-label': this.labelIndicators,
          'aria-owns': this.safeId('__BV_inner_')
        }
      }, this.slides.map(function (slide, n) {
        return h('li', {
          key: "slide_".concat(n),
          class: {
            active: n === _this3.index
          },
          attrs: {
            role: 'button',
            id: _this3.safeId("__BV_indicator_".concat(n + 1, "_")),
            tabindex: _this3.indicators ? '0' : '-1',
            'aria-current': n === _this3.index ? 'true' : 'false',
            'aria-label': "".concat(_this3.labelGotoSlide, " ").concat(n + 1),
            'aria-describedby': _this3.slides[n].id || null,
            'aria-controls': _this3.safeId('__BV_inner_')
          },
          on: {
            click: function click(evt) {
              _this3.handleClick(evt, function () {
                _this3.setSlide(n);
              });
            },
            keydown: function keydown(evt) {
              _this3.handleClick(evt, function () {
                _this3.setSlide(n);
              });
            }
          }
        });
      }));
      var on = {
        mouseenter: this.pause,
        mouseleave: this.restart,
        focusin: this.pause,
        focusout: this.restart,
        keydown: function keydown(evt) {
          if (/input|textarea/i.test(evt.target.tagName)) {
            return;
          }

          var keyCode = evt.keyCode;

          if (keyCode === KeyCodes.LEFT || keyCode === KeyCodes.RIGHT) {
            evt.preventDefault();
            evt.stopPropagation();

            _this3[keyCode === KeyCodes.LEFT ? 'prev' : 'next']();
          }
        } // Touch support event handlers for environment

      };

      if (!this.noTouch && hasTouchSupport) {
        /* istanbul ignore next: JSDOM doesn't support touch events */
        // Attach appropriate listeners (passsive mode)
        if (hasPointerEvent) {
          on['&pointerdown'] = this.touchStart;
          on['&pointerup'] = this.touchEnd;
        } else {
          on['&touchstart'] = this.touchStart;
          on['&touchmove'] = this.touchMove;
          on['&touchend'] = this.touchEnd;
        }
      } // Return the carousel


      return h('div', {
        staticClass: 'carousel',
        class: {
          slide: !this.noAnimation,
          'carousel-fade': !this.noAnimation && this.fade,
          'pointer-event': !this.noTouch && hasTouchSupport && hasPointerEvent
        },
        style: {
          background: this.background
        },
        attrs: {
          role: 'region',
          id: this.safeId(),
          'aria-busy': this.isSliding ? 'true' : 'false'
        },
        on: on
      }, [inner, controls, indicators]);
    }
  };

  var BLANK_TEMPLATE = '<svg width="%{w}" height="%{h}" ' + 'xmlns="http://www.w3.org/2000/svg" ' + 'viewBox="0 0 %{w} %{h}" preserveAspectRatio="none">' + '<rect width="100%" height="100%" style="fill:%{f};"></rect>' + '</svg>';

  function makeBlankImgSrc(width, height, color) {
    var src = encodeURIComponent(BLANK_TEMPLATE.replace('%{w}', String(width)).replace('%{h}', String(height)).replace('%{f}', color));
    return "data:image/svg+xml;charset=UTF-8,".concat(src);
  }

  var props$h = {
    src: {
      type: String,
      default: null
    },
    alt: {
      type: String,
      default: null
    },
    width: {
      type: [Number, String],
      default: null
    },
    height: {
      type: [Number, String],
      default: null
    },
    block: {
      type: Boolean,
      default: false
    },
    fluid: {
      type: Boolean,
      default: false
    },
    fluidGrow: {
      // Gives fluid images class `w-100` to make them grow to fit container
      type: Boolean,
      default: false
    },
    rounded: {
      // rounded can be:
      //   false: no rounding of corners
      //   true: slightly rounded corners
      //   'top': top corners rounded
      //   'right': right corners rounded
      //   'bottom': bottom corners rounded
      //   'left': left corners rounded
      //   'circle': circle/oval
      //   '0': force rounding off
      type: [Boolean, String],
      default: false
    },
    thumbnail: {
      type: Boolean,
      default: false
    },
    left: {
      type: Boolean,
      default: false
    },
    right: {
      type: Boolean,
      default: false
    },
    center: {
      type: Boolean,
      default: false
    },
    blank: {
      type: Boolean,
      default: false
    },
    blankColor: {
      type: String,
      default: 'transparent'
    } // @vue/component

  };
  var BImg = {
    name: 'BImg',
    functional: true,
    props: props$h,
    render: function render(h, _ref) {
      var _class;

      var props = _ref.props,
          data = _ref.data;
      var src = props.src;
      var width = parseInt(props.width, 10) ? parseInt(props.width, 10) : null;
      var height = parseInt(props.height, 10) ? parseInt(props.height, 10) : null;
      var align = null;
      var block = props.block;

      if (props.blank) {
        if (!height && Boolean(width)) {
          height = width;
        } else if (!width && Boolean(height)) {
          width = height;
        }

        if (!width && !height) {
          width = 1;
          height = 1;
        } // Make a blank SVG image


        src = makeBlankImgSrc(width, height, props.blankColor || 'transparent');
      }

      if (props.left) {
        align = 'float-left';
      } else if (props.right) {
        align = 'float-right';
      } else if (props.center) {
        align = 'mx-auto';
        block = true;
      }

      return h('img', mergeData(data, {
        attrs: {
          src: src,
          alt: props.alt,
          width: width ? String(width) : null,
          height: height ? String(height) : null
        },
        class: (_class = {
          'img-thumbnail': props.thumbnail,
          'img-fluid': props.fluid || props.fluidGrow,
          'w-100': props.fluidGrow,
          rounded: props.rounded === '' || props.rounded === true
        }, _defineProperty(_class, "rounded-".concat(props.rounded), typeof props.rounded === 'string' && props.rounded !== ''), _defineProperty(_class, align, Boolean(align)), _defineProperty(_class, 'd-block', block), _class)
      }));
    }
  };

  var BCarouselSlide = {
    name: 'BCarouselSlide',
    components: {
      BImg: BImg
    },
    mixins: [idMixin],
    inject: {
      carousel: {
        from: 'carousel',
        default: function _default() {
          return {
            // Explicitly disable touch if not a child of carousel
            noTouch: true
          };
        }
      }
    },
    props: {
      imgSrc: {
        type: String // default: undefined

      },
      imgAlt: {
        type: String // default: undefined

      },
      imgWidth: {
        type: [Number, String] // default: undefined

      },
      imgHeight: {
        type: [Number, String] // default: undefined

      },
      imgBlank: {
        type: Boolean,
        default: false
      },
      imgBlankColor: {
        type: String,
        default: 'transparent'
      },
      contentVisibleUp: {
        type: String
      },
      contentTag: {
        type: String,
        default: 'div'
      },
      caption: {
        type: String
      },
      captionHtml: {
        type: String
      },
      captionTag: {
        type: String,
        default: 'h3'
      },
      text: {
        type: String
      },
      textHtml: {
        type: String
      },
      textTag: {
        type: String,
        default: 'p'
      },
      background: {
        type: String
      }
    },
    data: function data() {
      return {};
    },
    computed: {
      contentClasses: function contentClasses() {
        return [this.contentVisibleUp ? 'd-none' : '', this.contentVisibleUp ? "d-".concat(this.contentVisibleUp, "-block") : ''];
      },
      computedWidth: function computedWidth() {
        // Use local width, or try parent width
        return this.imgWidth || this.carousel.imgWidth || null;
      },
      computedHeight: function computedHeight() {
        // Use local height, or try parent height
        return this.imgHeight || this.carousel.imgHeight || null;
      }
    },
    render: function render(h) {
      var $slots = this.$slots;
      var noDrag = !this.carousel.noTouch && hasTouchSupport;
      var img = $slots.img;

      if (!img && (this.imgSrc || this.imgBlank)) {
        img = h('b-img', {
          props: {
            fluidGrow: true,
            block: true,
            src: this.imgSrc,
            blank: this.imgBlank,
            blankColor: this.imgBlankColor,
            width: this.computedWidth,
            height: this.computedHeight,
            alt: this.imgAlt
          },
          // Touch support event handler
          on: noDrag ? {
            dragstart: function dragstart(e) {
              e.preventDefault();
            }
          } : {}
        });
      }

      if (!img) {
        img = h(false);
      }

      var content = h(this.contentTag, {
        staticClass: 'carousel-caption',
        class: this.contentClasses
      }, [this.caption || this.captionHtml ? h(this.captionTag, {
        domProps: htmlOrText(this.captionHtml, this.caption)
      }) : h(false), this.text || this.textHtml ? h(this.textTag, {
        domProps: htmlOrText(this.textHtml, this.text)
      }) : h(false), $slots.default]);
      return h('div', {
        staticClass: 'carousel-item',
        style: {
          background: this.background || this.carousel.background || null
        },
        attrs: {
          id: this.safeId(),
          role: 'listitem'
        }
      }, [img, content]);
    }
  };

  var components$8 = {
    BCarousel: BCarousel,
    BCarouselSlide: BCarouselSlide
  };
  var index$8 = {
    install: function install(Vue) {
      registerComponents(Vue, components$8);
    }
  };

  var props$i = {
    tag: {
      type: String,
      default: 'div'
    },
    fluid: {
      type: Boolean,
      default: false
    } // @vue/component

  };
  var Container = {
    name: 'BContainer',
    functional: true,
    props: props$i,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        class: {
          container: !props.fluid,
          'container-fluid': props.fluid
        }
      }), children);
    }
  };

  var COMMON_ALIGNMENT = ['start', 'end', 'center'];
  var props$j = {
    tag: {
      type: String,
      default: 'div'
    },
    noGutters: {
      type: Boolean,
      default: false
    },
    alignV: {
      type: String,
      default: null,
      validator: function validator(str) {
        return arrayIncludes(COMMON_ALIGNMENT.concat(['baseline', 'stretch']), str);
      }
    },
    alignH: {
      type: String,
      default: null,
      validator: function validator(str) {
        return arrayIncludes(COMMON_ALIGNMENT.concat(['between', 'around']), str);
      }
    },
    alignContent: {
      type: String,
      default: null,
      validator: function validator(str) {
        return arrayIncludes(COMMON_ALIGNMENT.concat(['between', 'around', 'stretch']), str);
      }
    } // @vue/component

  };
  var BRow = {
    name: 'BRow',
    functional: true,
    props: props$j,
    render: function render(h, _ref) {
      var _class;

      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        staticClass: 'row',
        class: (_class = {
          'no-gutters': props.noGutters
        }, _defineProperty(_class, "align-items-".concat(props.alignV), props.alignV), _defineProperty(_class, "justify-content-".concat(props.alignH), props.alignH), _defineProperty(_class, "align-content-".concat(props.alignContent), props.alignContent), _class)
      }), children);
    }
  };

  function memoize(fn) {
    var cache = create(null);
    return function memoizedFn() {
      var args = JSON.stringify(arguments);
      return cache[args] = cache[args] || fn.apply(null, arguments);
    };
  }

  /**
   * Suffix can be a falsey value so nothing is appended to string.
   * (helps when looping over props & some shouldn't change)
   * Use data last parameters to allow for currying.
   * @param {string} suffix
   * @param {string} str
   */

  function suffixPropName(suffix, str) {
    return str + (suffix ? upperFirst(suffix) : '');
  }

  /**
   * Generates a prop object with a type of
   * [Boolean, String, Number]
   */

  function boolStrNum() {
    return {
      type: [Boolean, String, Number],
      default: false
    };
  }
  /**
   * Generates a prop object with a type of
   * [String, Number]
   */


  function strNum() {
    return {
      type: [String, Number],
      default: null
    };
  }

  var computeBkPtClass = memoize(function computeBkPt(type, breakpoint, val) {
    var className = type;

    if (val === false || val === null || val === undefined) {
      return undefined;
    }

    if (breakpoint) {
      className += "-".concat(breakpoint);
    } // Handling the boolean style prop when accepting [Boolean, String, Number]
    // means Vue will not convert <b-col sm /> to sm: true for us.
    // Since the default is false, an empty string indicates the prop's presence.


    if (type === 'col' && (val === '' || val === true)) {
      // .col-md
      return className.toLowerCase();
    } // .order-md-6


    className += "-".concat(val);
    return className.toLowerCase();
  });
  var BREAKPOINTS = ['sm', 'md', 'lg', 'xl']; // Supports classes like: .col-sm, .col-md-6, .col-lg-auto

  var breakpointCol = BREAKPOINTS.reduce( // eslint-disable-next-line no-sequences
  function (propMap, breakpoint) {
    return propMap[breakpoint] = boolStrNum(), propMap;
  }, create(null)); // Supports classes like: .offset-md-1, .offset-lg-12

  var breakpointOffset = BREAKPOINTS.reduce( // eslint-disable-next-line no-sequences
  function (propMap, breakpoint) {
    return propMap[suffixPropName(breakpoint, 'offset')] = strNum(), propMap;
  }, create(null)); // Supports classes like: .order-md-1, .order-lg-12

  var breakpointOrder = BREAKPOINTS.reduce( // eslint-disable-next-line no-sequences
  function (propMap, breakpoint) {
    return propMap[suffixPropName(breakpoint, 'order')] = strNum(), propMap;
  }, create(null)); // For loop doesn't need to check hasOwnProperty
  // when using an object created from null

  var breakpointPropMap = assign(create(null), {
    col: keys(breakpointCol),
    offset: keys(breakpointOffset),
    order: keys(breakpointOrder)
  });
  var props$k = _objectSpread({}, breakpointCol, breakpointOffset, breakpointOrder, {
    tag: {
      type: String,
      default: 'div'
    },
    // Generic flexbox .col
    col: {
      type: Boolean,
      default: false
    },
    // .col-[1-12]|auto
    cols: strNum(),
    // .offset-[1-12]
    offset: strNum(),
    // Flex ordering utility .order-[1-12]
    order: strNum(),
    alignSelf: {
      type: String,
      default: null,
      validator: function validator(str) {
        return arrayIncludes(['auto', 'start', 'end', 'center', 'baseline', 'stretch'], str);
      }
    }
    /**
     * We need ".col" to default in when no other props are passed,
     * but always render when col=true.
     */
    // @vue/component

  });
  var BCol = {
    name: 'BCol',
    functional: true,
    props: props$k,
    render: function render(h, _ref) {
      var _classList$push;

      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var classList = []; // Loop through `col`, `offset`, `order` breakpoint props

      for (var type in breakpointPropMap) {
        // Returns colSm, offset, offsetSm, orderMd, etc.
        var _keys = breakpointPropMap[type];

        for (var i = 0; i < _keys.length; i++) {
          // computeBkPt(col, colSm => Sm, value=[String, Number, Boolean])
          var c = computeBkPtClass(type, _keys[i].replace(type, ''), props[_keys[i]]); // If a class is returned, push it onto the array.

          if (c) {
            classList.push(c);
          }
        }
      }

      classList.push((_classList$push = {
        // Default to .col if no other classes generated nor `cols` specified.
        col: props.col || classList.length === 0 && !props.cols
      }, _defineProperty(_classList$push, "col-".concat(props.cols), props.cols), _defineProperty(_classList$push, "offset-".concat(props.offset), props.offset), _defineProperty(_classList$push, "order-".concat(props.order), props.order), _defineProperty(_classList$push, "align-self-".concat(props.alignSelf), props.alignSelf), _classList$push));
      return h(props.tag, mergeData(data, {
        class: classList
      }), children);
    }
  };

  var props$l = {
    tag: {
      type: String,
      default: 'div'
    } // @vue/component

  };
  var BFormRow = {
    name: 'BFormRow',
    functional: true,
    props: props$l,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        staticClass: 'form-row'
      }), children);
    }
  };

  var components$9 = {
    BContainer: Container,
    BRow: BRow,
    BCol: BCol,
    BFormRow: BFormRow
  };
  var index$9 = {
    install: function install(Vue) {
      registerComponents(Vue, components$9);
    }
  };

  /**
   * Issue #569: collapse::toggle::state triggered too many times
   * @link https://github.com/bootstrap-vue/bootstrap-vue/issues/569
   */

  var BVRL = '__BV_root_listeners__'; // @vue/component

  var listenOnRootMixin = {
    beforeDestroy: function beforeDestroy() {
      if (this[BVRL] && isArray(this[BVRL])) {
        while (this[BVRL].length > 0) {
          // shift to process in order
          var _this$BVRL$shift = this[BVRL].shift(),
              event = _this$BVRL$shift.event,
              callback = _this$BVRL$shift.callback;

          this.$root.$off(event, callback);
        }
      }
    },
    methods: {
      /**
       * Safely register event listeners on the root Vue node.
       * While Vue automatically removes listeners for individual components,
       * when a component registers a listener on root and is destroyed,
       * this orphans a callback because the node is gone,
       * but the root does not clear the callback.
       *
       * This adds a non-reactive prop to a vm on the fly
       * in order to avoid object observation and its performance costs
       * to something that needs no reactivity.
       * It should be highly unlikely there are any naming collisions.
       * @param {string} event
       * @param {function} callback
       * @chainable
       */
      listenOnRoot: function listenOnRoot(event, callback) {
        if (!this[BVRL] || !isArray(this[BVRL])) {
          this[BVRL] = [];
        }

        this[BVRL].push({
          event: event,
          callback: callback
        });
        this.$root.$on(event, callback);
        return this;
      },

      /**
       * Convenience method for calling vm.$emit on vm.$root.
       * @param {string} event
       * @param {*} args
       * @chainable
       */
      emitOnRoot: function emitOnRoot(event) {
        var _this$$root;

        for (var _len = arguments.length, args = new Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
          args[_key - 1] = arguments[_key];
        }

        (_this$$root = this.$root).$emit.apply(_this$$root, [event].concat(args));

        return this;
      }
    }
  };

  var EVENT_STATE = 'bv::collapse::state';
  var EVENT_ACCORDION = 'bv::collapse::accordion'; // Events we listen to on $root

  var EVENT_TOGGLE = 'bv::toggle::collapse'; // Event Listener options

  var EventOptions$1 = {
    passive: true,
    capture: false // @vue/component

  };
  var BCollapse = {
    name: 'BCollapse',
    mixins: [listenOnRootMixin],
    model: {
      prop: 'visible',
      event: 'input'
    },
    props: {
      id: {
        type: String,
        required: true
      },
      isNav: {
        type: Boolean,
        default: false
      },
      accordion: {
        type: String,
        default: null
      },
      visible: {
        type: Boolean,
        default: false
      },
      tag: {
        type: String,
        default: 'div'
      }
    },
    data: function data() {
      return {
        show: this.visible,
        transitioning: false
      };
    },
    computed: {
      classObject: function classObject() {
        return {
          'navbar-collapse': this.isNav,
          collapse: !this.transitioning,
          show: this.show && !this.transitioning
        };
      }
    },
    watch: {
      visible: function visible(newVal) {
        if (newVal !== this.show) {
          this.show = newVal;
        }
      },
      show: function show(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.emitState();
        }
      }
    },
    created: function created() {
      // Listen for toggle events to open/close us
      this.listenOnRoot(EVENT_TOGGLE, this.handleToggleEvt); // Listen to other collapses for accordion events

      this.listenOnRoot(EVENT_ACCORDION, this.handleAccordionEvt);
    },
    mounted: function mounted() {
      if (this.isNav && typeof document !== 'undefined') {
        // Set up handlers
        eventOn(window, 'resize', this.handleResize, EventOptions$1);
        eventOn(window, 'orientationchange', this.handleResize, EventOptions$1);
        this.handleResize();
      }

      this.emitState();
    },
    updated: function updated() {
      this.$root.$emit(EVENT_STATE, this.id, this.show);
    },
    beforeDestroy: function beforeDestroy()
    /* istanbul ignore next */
    {
      if (this.isNav && typeof document !== 'undefined') {
        eventOff(window, 'resize', this.handleResize, EventOptions$1);
        eventOff(window, 'orientationchange', this.handleResize, EventOptions$1);
      }
    },
    methods: {
      toggle: function toggle() {
        this.show = !this.show;
      },
      onEnter: function onEnter(el) {
        el.style.height = 0;
        reflow(el);
        el.style.height = el.scrollHeight + 'px';
        this.transitioning = true; // This should be moved out so we can add cancellable events

        this.$emit('show');
      },
      onAfterEnter: function onAfterEnter(el) {
        el.style.height = null;
        this.transitioning = false;
        this.$emit('shown');
      },
      onLeave: function onLeave(el) {
        el.style.height = 'auto';
        el.style.display = 'block';
        el.style.height = getBCR(el).height + 'px';
        reflow(el);
        this.transitioning = true;
        el.style.height = 0; // This should be moved out so we can add cancellable events

        this.$emit('hide');
      },
      onAfterLeave: function onAfterLeave(el) {
        el.style.height = null;
        this.transitioning = false;
        this.$emit('hidden');
      },
      emitState: function emitState() {
        this.$emit('input', this.show); // Let v-b-toggle know the state of this collapse

        this.$root.$emit(EVENT_STATE, this.id, this.show);

        if (this.accordion && this.show) {
          // Tell the other collapses in this accordion to close
          this.$root.$emit(EVENT_ACCORDION, this.id, this.accordion);
        }
      },
      clickHandler: function clickHandler(evt) {
        // If we are in a nav/navbar, close the collapse when non-disabled link clicked
        var el = evt.target;

        if (!this.isNav || !el || getCS(this.$el).display !== 'block') {
          return;
        }

        if (matches(el, '.nav-link,.dropdown-item') || closest('.nav-link,.dropdown-item', el)) {
          this.show = false;
        }
      },
      handleToggleEvt: function handleToggleEvt(target) {
        if (target !== this.id) {
          return;
        }

        this.toggle();
      },
      handleAccordionEvt: function handleAccordionEvt(openedId, accordion) {
        if (!this.accordion || accordion !== this.accordion) {
          return;
        }

        if (openedId === this.id) {
          // Open this collapse if not shown
          if (!this.show) {
            this.toggle();
          }
        } else {
          // Close this collapse if shown
          if (this.show) {
            this.toggle();
          }
        }
      },
      handleResize: function handleResize() {
        // Handler for orientation/resize to set collapsed state in nav/navbar
        this.show = getCS(this.$el).display === 'block';
      }
    },
    render: function render(h) {
      var content = h(this.tag, {
        class: this.classObject,
        directives: [{
          name: 'show',
          value: this.show
        }],
        attrs: {
          id: this.id || null
        },
        on: {
          click: this.clickHandler
        }
      }, [this.$slots.default]);
      return h('transition', {
        props: {
          enterClass: '',
          enterActiveClass: 'collapsing',
          enterToClass: '',
          leaveClass: '',
          leaveActiveClass: 'collapsing',
          leaveToClass: ''
        },
        on: {
          enter: this.onEnter,
          afterEnter: this.onAfterEnter,
          leave: this.onLeave,
          afterLeave: this.onAfterLeave
        }
      }, [content]);
    }
  };

  var allListenTypes = {
    hover: true,
    click: true,
    focus: true
  };
  var BVBoundListeners = '__BV_boundEventListeners__';

  var bindTargets = function bindTargets(vnode, binding, listenTypes, fn) {
    var targets = keys(binding.modifiers || {}).filter(function (t) {
      return !allListenTypes[t];
    });

    if (binding.value) {
      targets.push(binding.value);
    }

    var listener = function listener() {
      fn({
        targets: targets,
        vnode: vnode
      });
    };

    keys(allListenTypes).forEach(function (type) {
      if (listenTypes[type] || binding.modifiers[type]) {
        eventOn(vnode.elm, type, listener);
        var boundListeners = vnode.elm[BVBoundListeners] || {};
        boundListeners[type] = boundListeners[type] || [];
        boundListeners[type].push(listener);
        vnode.elm[BVBoundListeners] = boundListeners;
      }
    }); // Return the list of targets

    return targets;
  };

  var unbindTargets = function unbindTargets(vnode, binding, listenTypes) {
    keys(allListenTypes).forEach(function (type) {
      if (listenTypes[type] || binding.modifiers[type]) {
        var boundListeners = vnode.elm[BVBoundListeners] && vnode.elm[BVBoundListeners][type];

        if (boundListeners) {
          boundListeners.forEach(function (listener) {
            return eventOff(vnode.elm, type, listener);
          });
          delete vnode.elm[BVBoundListeners][type];
        }
      }
    });
  };

  var inBrowser$1 = typeof window !== 'undefined'; // target listen types

  var listenTypes = {
    click: true // Property key for handler storage

  };
  var BVT = '__BV_toggle__'; // Emitted Control Event for collapse (emitted to collapse)

  var EVENT_TOGGLE$1 = 'bv::toggle::collapse'; // Listen to Event for toggle state update (Emited by collapse)

  var EVENT_STATE$1 = 'bv::collapse::state';
  var bToggle = {
    bind: function bind(el, binding, vnode) {
      var targets = bindTargets(vnode, binding, listenTypes, function (_ref) {
        var targets = _ref.targets,
            vnode = _ref.vnode;
        targets.forEach(function (target) {
          vnode.context.$root.$emit(EVENT_TOGGLE$1, target);
        });
      });

      if (inBrowser$1 && vnode.context && targets.length > 0) {
        // Add aria attributes to element
        setAttr(el, 'aria-controls', targets.join(' '));
        setAttr(el, 'aria-expanded', 'false');

        if (el.tagName !== 'BUTTON') {
          // If element is not a button, we add `role="button"` for accessibility
          setAttr(el, 'role', 'button');
        } // Toggle state hadnler, stored on element


        el[BVT] = function toggleDirectiveHandler(id, state) {
          if (targets.indexOf(id) !== -1) {
            // Set aria-expanded state
            setAttr(el, 'aria-expanded', state ? 'true' : 'false'); // Set/Clear 'collapsed' class state

            if (state) {
              removeClass(el, 'collapsed');
            } else {
              addClass(el, 'collapsed');
            }
          }
        }; // Listen for toggle state changes


        vnode.context.$root.$on(EVENT_STATE$1, el[BVT]);
      }
    },
    unbind: function unbind(el, binding, vnode) {
      if (el[BVT]) {
        // Remove our $root listener
        vnode.context.$root.$off(EVENT_STATE$1, el[BVT]);
        el[BVT] = null;
      }
    }
  };

  var directives = {
    bToggle: bToggle
  };
  var toggleDirectivePlugin = {
    install: function install(Vue) {
      registerDirectives(Vue, directives);
    }
  };

  var components$a = {
    BCollapse: BCollapse
  };
  var collapsePlugin = {
    install: function install(Vue) {
      registerComponents(Vue, components$a);
      Vue.use(toggleDirectivePlugin);
    }
  };

  /**!
   * @fileOverview Kickass library to create and place poppers near their reference elements.
   * @version 1.14.7
   * @license
   * Copyright (c) 2016 Federico Zivolo and contributors
   *
   * Permission is hereby granted, free of charge, to any person obtaining a copy
   * of this software and associated documentation files (the "Software"), to deal
   * in the Software without restriction, including without limitation the rights
   * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   * copies of the Software, and to permit persons to whom the Software is
   * furnished to do so, subject to the following conditions:
   *
   * The above copyright notice and this permission notice shall be included in all
   * copies or substantial portions of the Software.
   *
   * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   * SOFTWARE.
   */
  var isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined';

  var longerTimeoutBrowsers = ['Edge', 'Trident', 'Firefox'];
  var timeoutDuration = 0;
  for (var i = 0; i < longerTimeoutBrowsers.length; i += 1) {
    if (isBrowser && navigator.userAgent.indexOf(longerTimeoutBrowsers[i]) >= 0) {
      timeoutDuration = 1;
      break;
    }
  }

  function microtaskDebounce(fn) {
    var called = false;
    return function () {
      if (called) {
        return;
      }
      called = true;
      window.Promise.resolve().then(function () {
        called = false;
        fn();
      });
    };
  }

  function taskDebounce(fn) {
    var scheduled = false;
    return function () {
      if (!scheduled) {
        scheduled = true;
        setTimeout(function () {
          scheduled = false;
          fn();
        }, timeoutDuration);
      }
    };
  }

  var supportsMicroTasks = isBrowser && window.Promise;

  /**
  * Create a debounced version of a method, that's asynchronously deferred
  * but called in the minimum time possible.
  *
  * @method
  * @memberof Popper.Utils
  * @argument {Function} fn
  * @returns {Function}
  */
  var debounce = supportsMicroTasks ? microtaskDebounce : taskDebounce;

  /**
   * Check if the given variable is a function
   * @method
   * @memberof Popper.Utils
   * @argument {Any} functionToCheck - variable to check
   * @returns {Boolean} answer to: is a function?
   */
  function isFunction(functionToCheck) {
    var getType = {};
    return functionToCheck && getType.toString.call(functionToCheck) === '[object Function]';
  }

  /**
   * Get CSS computed property of the given element
   * @method
   * @memberof Popper.Utils
   * @argument {Eement} element
   * @argument {String} property
   */
  function getStyleComputedProperty(element, property) {
    if (element.nodeType !== 1) {
      return [];
    }
    // NOTE: 1 DOM access here
    var window = element.ownerDocument.defaultView;
    var css = window.getComputedStyle(element, null);
    return property ? css[property] : css;
  }

  /**
   * Returns the parentNode or the host of the element
   * @method
   * @memberof Popper.Utils
   * @argument {Element} element
   * @returns {Element} parent
   */
  function getParentNode(element) {
    if (element.nodeName === 'HTML') {
      return element;
    }
    return element.parentNode || element.host;
  }

  /**
   * Returns the scrolling parent of the given element
   * @method
   * @memberof Popper.Utils
   * @argument {Element} element
   * @returns {Element} scroll parent
   */
  function getScrollParent(element) {
    // Return body, `getScroll` will take care to get the correct `scrollTop` from it
    if (!element) {
      return document.body;
    }

    switch (element.nodeName) {
      case 'HTML':
      case 'BODY':
        return element.ownerDocument.body;
      case '#document':
        return element.body;
    }

    // Firefox want us to check `-x` and `-y` variations as well

    var _getStyleComputedProp = getStyleComputedProperty(element),
        overflow = _getStyleComputedProp.overflow,
        overflowX = _getStyleComputedProp.overflowX,
        overflowY = _getStyleComputedProp.overflowY;

    if (/(auto|scroll|overlay)/.test(overflow + overflowY + overflowX)) {
      return element;
    }

    return getScrollParent(getParentNode(element));
  }

  var isIE11 = isBrowser && !!(window.MSInputMethodContext && document.documentMode);
  var isIE10 = isBrowser && /MSIE 10/.test(navigator.userAgent);

  /**
   * Determines if the browser is Internet Explorer
   * @method
   * @memberof Popper.Utils
   * @param {Number} version to check
   * @returns {Boolean} isIE
   */
  function isIE(version) {
    if (version === 11) {
      return isIE11;
    }
    if (version === 10) {
      return isIE10;
    }
    return isIE11 || isIE10;
  }

  /**
   * Returns the offset parent of the given element
   * @method
   * @memberof Popper.Utils
   * @argument {Element} element
   * @returns {Element} offset parent
   */
  function getOffsetParent(element) {
    if (!element) {
      return document.documentElement;
    }

    var noOffsetParent = isIE(10) ? document.body : null;

    // NOTE: 1 DOM access here
    var offsetParent = element.offsetParent || null;
    // Skip hidden elements which don't have an offsetParent
    while (offsetParent === noOffsetParent && element.nextElementSibling) {
      offsetParent = (element = element.nextElementSibling).offsetParent;
    }

    var nodeName = offsetParent && offsetParent.nodeName;

    if (!nodeName || nodeName === 'BODY' || nodeName === 'HTML') {
      return element ? element.ownerDocument.documentElement : document.documentElement;
    }

    // .offsetParent will return the closest TH, TD or TABLE in case
    // no offsetParent is present, I hate this job...
    if (['TH', 'TD', 'TABLE'].indexOf(offsetParent.nodeName) !== -1 && getStyleComputedProperty(offsetParent, 'position') === 'static') {
      return getOffsetParent(offsetParent);
    }

    return offsetParent;
  }

  function isOffsetContainer(element) {
    var nodeName = element.nodeName;

    if (nodeName === 'BODY') {
      return false;
    }
    return nodeName === 'HTML' || getOffsetParent(element.firstElementChild) === element;
  }

  /**
   * Finds the root node (document, shadowDOM root) of the given element
   * @method
   * @memberof Popper.Utils
   * @argument {Element} node
   * @returns {Element} root node
   */
  function getRoot(node) {
    if (node.parentNode !== null) {
      return getRoot(node.parentNode);
    }

    return node;
  }

  /**
   * Finds the offset parent common to the two provided nodes
   * @method
   * @memberof Popper.Utils
   * @argument {Element} element1
   * @argument {Element} element2
   * @returns {Element} common offset parent
   */
  function findCommonOffsetParent(element1, element2) {
    // This check is needed to avoid errors in case one of the elements isn't defined for any reason
    if (!element1 || !element1.nodeType || !element2 || !element2.nodeType) {
      return document.documentElement;
    }

    // Here we make sure to give as "start" the element that comes first in the DOM
    var order = element1.compareDocumentPosition(element2) & Node.DOCUMENT_POSITION_FOLLOWING;
    var start = order ? element1 : element2;
    var end = order ? element2 : element1;

    // Get common ancestor container
    var range = document.createRange();
    range.setStart(start, 0);
    range.setEnd(end, 0);
    var commonAncestorContainer = range.commonAncestorContainer;

    // Both nodes are inside #document

    if (element1 !== commonAncestorContainer && element2 !== commonAncestorContainer || start.contains(end)) {
      if (isOffsetContainer(commonAncestorContainer)) {
        return commonAncestorContainer;
      }

      return getOffsetParent(commonAncestorContainer);
    }

    // one of the nodes is inside shadowDOM, find which one
    var element1root = getRoot(element1);
    if (element1root.host) {
      return findCommonOffsetParent(element1root.host, element2);
    } else {
      return findCommonOffsetParent(element1, getRoot(element2).host);
    }
  }

  /**
   * Gets the scroll value of the given element in the given side (top and left)
   * @method
   * @memberof Popper.Utils
   * @argument {Element} element
   * @argument {String} side `top` or `left`
   * @returns {number} amount of scrolled pixels
   */
  function getScroll(element) {
    var side = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'top';

    var upperSide = side === 'top' ? 'scrollTop' : 'scrollLeft';
    var nodeName = element.nodeName;

    if (nodeName === 'BODY' || nodeName === 'HTML') {
      var html = element.ownerDocument.documentElement;
      var scrollingElement = element.ownerDocument.scrollingElement || html;
      return scrollingElement[upperSide];
    }

    return element[upperSide];
  }

  /*
   * Sum or subtract the element scroll values (left and top) from a given rect object
   * @method
   * @memberof Popper.Utils
   * @param {Object} rect - Rect object you want to change
   * @param {HTMLElement} element - The element from the function reads the scroll values
   * @param {Boolean} subtract - set to true if you want to subtract the scroll values
   * @return {Object} rect - The modifier rect object
   */
  function includeScroll(rect, element) {
    var subtract = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;

    var scrollTop = getScroll(element, 'top');
    var scrollLeft = getScroll(element, 'left');
    var modifier = subtract ? -1 : 1;
    rect.top += scrollTop * modifier;
    rect.bottom += scrollTop * modifier;
    rect.left += scrollLeft * modifier;
    rect.right += scrollLeft * modifier;
    return rect;
  }

  /*
   * Helper to detect borders of a given element
   * @method
   * @memberof Popper.Utils
   * @param {CSSStyleDeclaration} styles
   * Result of `getStyleComputedProperty` on the given element
   * @param {String} axis - `x` or `y`
   * @return {number} borders - The borders size of the given axis
   */

  function getBordersSize(styles, axis) {
    var sideA = axis === 'x' ? 'Left' : 'Top';
    var sideB = sideA === 'Left' ? 'Right' : 'Bottom';

    return parseFloat(styles['border' + sideA + 'Width'], 10) + parseFloat(styles['border' + sideB + 'Width'], 10);
  }

  function getSize(axis, body, html, computedStyle) {
    return Math.max(body['offset' + axis], body['scroll' + axis], html['client' + axis], html['offset' + axis], html['scroll' + axis], isIE(10) ? parseInt(html['offset' + axis]) + parseInt(computedStyle['margin' + (axis === 'Height' ? 'Top' : 'Left')]) + parseInt(computedStyle['margin' + (axis === 'Height' ? 'Bottom' : 'Right')]) : 0);
  }

  function getWindowSizes(document) {
    var body = document.body;
    var html = document.documentElement;
    var computedStyle = isIE(10) && getComputedStyle(html);

    return {
      height: getSize('Height', body, html, computedStyle),
      width: getSize('Width', body, html, computedStyle)
    };
  }

  var classCallCheck = function (instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  };

  var createClass = function () {
    function defineProperties(target, props) {
      for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
      }
    }

    return function (Constructor, protoProps, staticProps) {
      if (protoProps) defineProperties(Constructor.prototype, protoProps);
      if (staticProps) defineProperties(Constructor, staticProps);
      return Constructor;
    };
  }();





  var defineProperty$1 = function (obj, key, value) {
    if (key in obj) {
      Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
      });
    } else {
      obj[key] = value;
    }

    return obj;
  };

  var _extends = Object.assign || function (target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i];

      for (var key in source) {
        if (Object.prototype.hasOwnProperty.call(source, key)) {
          target[key] = source[key];
        }
      }
    }

    return target;
  };

  /**
   * Given element offsets, generate an output similar to getBoundingClientRect
   * @method
   * @memberof Popper.Utils
   * @argument {Object} offsets
   * @returns {Object} ClientRect like output
   */
  function getClientRect(offsets) {
    return _extends({}, offsets, {
      right: offsets.left + offsets.width,
      bottom: offsets.top + offsets.height
    });
  }

  /**
   * Get bounding client rect of given element
   * @method
   * @memberof Popper.Utils
   * @param {HTMLElement} element
   * @return {Object} client rect
   */
  function getBoundingClientRect(element) {
    var rect = {};

    // IE10 10 FIX: Please, don't ask, the element isn't
    // considered in DOM in some circumstances...
    // This isn't reproducible in IE10 compatibility mode of IE11
    try {
      if (isIE(10)) {
        rect = element.getBoundingClientRect();
        var scrollTop = getScroll(element, 'top');
        var scrollLeft = getScroll(element, 'left');
        rect.top += scrollTop;
        rect.left += scrollLeft;
        rect.bottom += scrollTop;
        rect.right += scrollLeft;
      } else {
        rect = element.getBoundingClientRect();
      }
    } catch (e) {}

    var result = {
      left: rect.left,
      top: rect.top,
      width: rect.right - rect.left,
      height: rect.bottom - rect.top
    };

    // subtract scrollbar size from sizes
    var sizes = element.nodeName === 'HTML' ? getWindowSizes(element.ownerDocument) : {};
    var width = sizes.width || element.clientWidth || result.right - result.left;
    var height = sizes.height || element.clientHeight || result.bottom - result.top;

    var horizScrollbar = element.offsetWidth - width;
    var vertScrollbar = element.offsetHeight - height;

    // if an hypothetical scrollbar is detected, we must be sure it's not a `border`
    // we make this check conditional for performance reasons
    if (horizScrollbar || vertScrollbar) {
      var styles = getStyleComputedProperty(element);
      horizScrollbar -= getBordersSize(styles, 'x');
      vertScrollbar -= getBordersSize(styles, 'y');

      result.width -= horizScrollbar;
      result.height -= vertScrollbar;
    }

    return getClientRect(result);
  }

  function getOffsetRectRelativeToArbitraryNode(children, parent) {
    var fixedPosition = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;

    var isIE10 = isIE(10);
    var isHTML = parent.nodeName === 'HTML';
    var childrenRect = getBoundingClientRect(children);
    var parentRect = getBoundingClientRect(parent);
    var scrollParent = getScrollParent(children);

    var styles = getStyleComputedProperty(parent);
    var borderTopWidth = parseFloat(styles.borderTopWidth, 10);
    var borderLeftWidth = parseFloat(styles.borderLeftWidth, 10);

    // In cases where the parent is fixed, we must ignore negative scroll in offset calc
    if (fixedPosition && isHTML) {
      parentRect.top = Math.max(parentRect.top, 0);
      parentRect.left = Math.max(parentRect.left, 0);
    }
    var offsets = getClientRect({
      top: childrenRect.top - parentRect.top - borderTopWidth,
      left: childrenRect.left - parentRect.left - borderLeftWidth,
      width: childrenRect.width,
      height: childrenRect.height
    });
    offsets.marginTop = 0;
    offsets.marginLeft = 0;

    // Subtract margins of documentElement in case it's being used as parent
    // we do this only on HTML because it's the only element that behaves
    // differently when margins are applied to it. The margins are included in
    // the box of the documentElement, in the other cases not.
    if (!isIE10 && isHTML) {
      var marginTop = parseFloat(styles.marginTop, 10);
      var marginLeft = parseFloat(styles.marginLeft, 10);

      offsets.top -= borderTopWidth - marginTop;
      offsets.bottom -= borderTopWidth - marginTop;
      offsets.left -= borderLeftWidth - marginLeft;
      offsets.right -= borderLeftWidth - marginLeft;

      // Attach marginTop and marginLeft because in some circumstances we may need them
      offsets.marginTop = marginTop;
      offsets.marginLeft = marginLeft;
    }

    if (isIE10 && !fixedPosition ? parent.contains(scrollParent) : parent === scrollParent && scrollParent.nodeName !== 'BODY') {
      offsets = includeScroll(offsets, parent);
    }

    return offsets;
  }

  function getViewportOffsetRectRelativeToArtbitraryNode(element) {
    var excludeScroll = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;

    var html = element.ownerDocument.documentElement;
    var relativeOffset = getOffsetRectRelativeToArbitraryNode(element, html);
    var width = Math.max(html.clientWidth, window.innerWidth || 0);
    var height = Math.max(html.clientHeight, window.innerHeight || 0);

    var scrollTop = !excludeScroll ? getScroll(html) : 0;
    var scrollLeft = !excludeScroll ? getScroll(html, 'left') : 0;

    var offset = {
      top: scrollTop - relativeOffset.top + relativeOffset.marginTop,
      left: scrollLeft - relativeOffset.left + relativeOffset.marginLeft,
      width: width,
      height: height
    };

    return getClientRect(offset);
  }

  /**
   * Check if the given element is fixed or is inside a fixed parent
   * @method
   * @memberof Popper.Utils
   * @argument {Element} element
   * @argument {Element} customContainer
   * @returns {Boolean} answer to "isFixed?"
   */
  function isFixed(element) {
    var nodeName = element.nodeName;
    if (nodeName === 'BODY' || nodeName === 'HTML') {
      return false;
    }
    if (getStyleComputedProperty(element, 'position') === 'fixed') {
      return true;
    }
    var parentNode = getParentNode(element);
    if (!parentNode) {
      return false;
    }
    return isFixed(parentNode);
  }

  /**
   * Finds the first parent of an element that has a transformed property defined
   * @method
   * @memberof Popper.Utils
   * @argument {Element} element
   * @returns {Element} first transformed parent or documentElement
   */

  function getFixedPositionOffsetParent(element) {
    // This check is needed to avoid errors in case one of the elements isn't defined for any reason
    if (!element || !element.parentElement || isIE()) {
      return document.documentElement;
    }
    var el = element.parentElement;
    while (el && getStyleComputedProperty(el, 'transform') === 'none') {
      el = el.parentElement;
    }
    return el || document.documentElement;
  }

  /**
   * Computed the boundaries limits and return them
   * @method
   * @memberof Popper.Utils
   * @param {HTMLElement} popper
   * @param {HTMLElement} reference
   * @param {number} padding
   * @param {HTMLElement} boundariesElement - Element used to define the boundaries
   * @param {Boolean} fixedPosition - Is in fixed position mode
   * @returns {Object} Coordinates of the boundaries
   */
  function getBoundaries(popper, reference, padding, boundariesElement) {
    var fixedPosition = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : false;

    // NOTE: 1 DOM access here

    var boundaries = { top: 0, left: 0 };
    var offsetParent = fixedPosition ? getFixedPositionOffsetParent(popper) : findCommonOffsetParent(popper, reference);

    // Handle viewport case
    if (boundariesElement === 'viewport') {
      boundaries = getViewportOffsetRectRelativeToArtbitraryNode(offsetParent, fixedPosition);
    } else {
      // Handle other cases based on DOM element used as boundaries
      var boundariesNode = void 0;
      if (boundariesElement === 'scrollParent') {
        boundariesNode = getScrollParent(getParentNode(reference));
        if (boundariesNode.nodeName === 'BODY') {
          boundariesNode = popper.ownerDocument.documentElement;
        }
      } else if (boundariesElement === 'window') {
        boundariesNode = popper.ownerDocument.documentElement;
      } else {
        boundariesNode = boundariesElement;
      }

      var offsets = getOffsetRectRelativeToArbitraryNode(boundariesNode, offsetParent, fixedPosition);

      // In case of HTML, we need a different computation
      if (boundariesNode.nodeName === 'HTML' && !isFixed(offsetParent)) {
        var _getWindowSizes = getWindowSizes(popper.ownerDocument),
            height = _getWindowSizes.height,
            width = _getWindowSizes.width;

        boundaries.top += offsets.top - offsets.marginTop;
        boundaries.bottom = height + offsets.top;
        boundaries.left += offsets.left - offsets.marginLeft;
        boundaries.right = width + offsets.left;
      } else {
        // for all the other DOM elements, this one is good
        boundaries = offsets;
      }
    }

    // Add paddings
    padding = padding || 0;
    var isPaddingNumber = typeof padding === 'number';
    boundaries.left += isPaddingNumber ? padding : padding.left || 0;
    boundaries.top += isPaddingNumber ? padding : padding.top || 0;
    boundaries.right -= isPaddingNumber ? padding : padding.right || 0;
    boundaries.bottom -= isPaddingNumber ? padding : padding.bottom || 0;

    return boundaries;
  }

  function getArea(_ref) {
    var width = _ref.width,
        height = _ref.height;

    return width * height;
  }

  /**
   * Utility used to transform the `auto` placement to the placement with more
   * available space.
   * @method
   * @memberof Popper.Utils
   * @argument {Object} data - The data object generated by update method
   * @argument {Object} options - Modifiers configuration and options
   * @returns {Object} The data object, properly modified
   */
  function computeAutoPlacement(placement, refRect, popper, reference, boundariesElement) {
    var padding = arguments.length > 5 && arguments[5] !== undefined ? arguments[5] : 0;

    if (placement.indexOf('auto') === -1) {
      return placement;
    }

    var boundaries = getBoundaries(popper, reference, padding, boundariesElement);

    var rects = {
      top: {
        width: boundaries.width,
        height: refRect.top - boundaries.top
      },
      right: {
        width: boundaries.right - refRect.right,
        height: boundaries.height
      },
      bottom: {
        width: boundaries.width,
        height: boundaries.bottom - refRect.bottom
      },
      left: {
        width: refRect.left - boundaries.left,
        height: boundaries.height
      }
    };

    var sortedAreas = Object.keys(rects).map(function (key) {
      return _extends({
        key: key
      }, rects[key], {
        area: getArea(rects[key])
      });
    }).sort(function (a, b) {
      return b.area - a.area;
    });

    var filteredAreas = sortedAreas.filter(function (_ref2) {
      var width = _ref2.width,
          height = _ref2.height;
      return width >= popper.clientWidth && height >= popper.clientHeight;
    });

    var computedPlacement = filteredAreas.length > 0 ? filteredAreas[0].key : sortedAreas[0].key;

    var variation = placement.split('-')[1];

    return computedPlacement + (variation ? '-' + variation : '');
  }

  /**
   * Get offsets to the reference element
   * @method
   * @memberof Popper.Utils
   * @param {Object} state
   * @param {Element} popper - the popper element
   * @param {Element} reference - the reference element (the popper will be relative to this)
   * @param {Element} fixedPosition - is in fixed position mode
   * @returns {Object} An object containing the offsets which will be applied to the popper
   */
  function getReferenceOffsets(state, popper, reference) {
    var fixedPosition = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : null;

    var commonOffsetParent = fixedPosition ? getFixedPositionOffsetParent(popper) : findCommonOffsetParent(popper, reference);
    return getOffsetRectRelativeToArbitraryNode(reference, commonOffsetParent, fixedPosition);
  }

  /**
   * Get the outer sizes of the given element (offset size + margins)
   * @method
   * @memberof Popper.Utils
   * @argument {Element} element
   * @returns {Object} object containing width and height properties
   */
  function getOuterSizes(element) {
    var window = element.ownerDocument.defaultView;
    var styles = window.getComputedStyle(element);
    var x = parseFloat(styles.marginTop || 0) + parseFloat(styles.marginBottom || 0);
    var y = parseFloat(styles.marginLeft || 0) + parseFloat(styles.marginRight || 0);
    var result = {
      width: element.offsetWidth + y,
      height: element.offsetHeight + x
    };
    return result;
  }

  /**
   * Get the opposite placement of the given one
   * @method
   * @memberof Popper.Utils
   * @argument {String} placement
   * @returns {String} flipped placement
   */
  function getOppositePlacement(placement) {
    var hash = { left: 'right', right: 'left', bottom: 'top', top: 'bottom' };
    return placement.replace(/left|right|bottom|top/g, function (matched) {
      return hash[matched];
    });
  }

  /**
   * Get offsets to the popper
   * @method
   * @memberof Popper.Utils
   * @param {Object} position - CSS position the Popper will get applied
   * @param {HTMLElement} popper - the popper element
   * @param {Object} referenceOffsets - the reference offsets (the popper will be relative to this)
   * @param {String} placement - one of the valid placement options
   * @returns {Object} popperOffsets - An object containing the offsets which will be applied to the popper
   */
  function getPopperOffsets(popper, referenceOffsets, placement) {
    placement = placement.split('-')[0];

    // Get popper node sizes
    var popperRect = getOuterSizes(popper);

    // Add position, width and height to our offsets object
    var popperOffsets = {
      width: popperRect.width,
      height: popperRect.height
    };

    // depending by the popper placement we have to compute its offsets slightly differently
    var isHoriz = ['right', 'left'].indexOf(placement) !== -1;
    var mainSide = isHoriz ? 'top' : 'left';
    var secondarySide = isHoriz ? 'left' : 'top';
    var measurement = isHoriz ? 'height' : 'width';
    var secondaryMeasurement = !isHoriz ? 'height' : 'width';

    popperOffsets[mainSide] = referenceOffsets[mainSide] + referenceOffsets[measurement] / 2 - popperRect[measurement] / 2;
    if (placement === secondarySide) {
      popperOffsets[secondarySide] = referenceOffsets[secondarySide] - popperRect[secondaryMeasurement];
    } else {
      popperOffsets[secondarySide] = referenceOffsets[getOppositePlacement(secondarySide)];
    }

    return popperOffsets;
  }

  /**
   * Mimics the `find` method of Array
   * @method
   * @memberof Popper.Utils
   * @argument {Array} arr
   * @argument prop
   * @argument value
   * @returns index or -1
   */
  function find(arr, check) {
    // use native find if supported
    if (Array.prototype.find) {
      return arr.find(check);
    }

    // use `filter` to obtain the same behavior of `find`
    return arr.filter(check)[0];
  }

  /**
   * Return the index of the matching object
   * @method
   * @memberof Popper.Utils
   * @argument {Array} arr
   * @argument prop
   * @argument value
   * @returns index or -1
   */
  function findIndex(arr, prop, value) {
    // use native findIndex if supported
    if (Array.prototype.findIndex) {
      return arr.findIndex(function (cur) {
        return cur[prop] === value;
      });
    }

    // use `find` + `indexOf` if `findIndex` isn't supported
    var match = find(arr, function (obj) {
      return obj[prop] === value;
    });
    return arr.indexOf(match);
  }

  /**
   * Loop trough the list of modifiers and run them in order,
   * each of them will then edit the data object.
   * @method
   * @memberof Popper.Utils
   * @param {dataObject} data
   * @param {Array} modifiers
   * @param {String} ends - Optional modifier name used as stopper
   * @returns {dataObject}
   */
  function runModifiers(modifiers, data, ends) {
    var modifiersToRun = ends === undefined ? modifiers : modifiers.slice(0, findIndex(modifiers, 'name', ends));

    modifiersToRun.forEach(function (modifier) {
      if (modifier['function']) {
        // eslint-disable-line dot-notation
        console.warn('`modifier.function` is deprecated, use `modifier.fn`!');
      }
      var fn = modifier['function'] || modifier.fn; // eslint-disable-line dot-notation
      if (modifier.enabled && isFunction(fn)) {
        // Add properties to offsets to make them a complete clientRect object
        // we do this before each modifier to make sure the previous one doesn't
        // mess with these values
        data.offsets.popper = getClientRect(data.offsets.popper);
        data.offsets.reference = getClientRect(data.offsets.reference);

        data = fn(data, modifier);
      }
    });

    return data;
  }

  /**
   * Updates the position of the popper, computing the new offsets and applying
   * the new style.<br />
   * Prefer `scheduleUpdate` over `update` because of performance reasons.
   * @method
   * @memberof Popper
   */
  function update() {
    // if popper is destroyed, don't perform any further update
    if (this.state.isDestroyed) {
      return;
    }

    var data = {
      instance: this,
      styles: {},
      arrowStyles: {},
      attributes: {},
      flipped: false,
      offsets: {}
    };

    // compute reference element offsets
    data.offsets.reference = getReferenceOffsets(this.state, this.popper, this.reference, this.options.positionFixed);

    // compute auto placement, store placement inside the data object,
    // modifiers will be able to edit `placement` if needed
    // and refer to originalPlacement to know the original value
    data.placement = computeAutoPlacement(this.options.placement, data.offsets.reference, this.popper, this.reference, this.options.modifiers.flip.boundariesElement, this.options.modifiers.flip.padding);

    // store the computed placement inside `originalPlacement`
    data.originalPlacement = data.placement;

    data.positionFixed = this.options.positionFixed;

    // compute the popper offsets
    data.offsets.popper = getPopperOffsets(this.popper, data.offsets.reference, data.placement);

    data.offsets.popper.position = this.options.positionFixed ? 'fixed' : 'absolute';

    // run the modifiers
    data = runModifiers(this.modifiers, data);

    // the first `update` will call `onCreate` callback
    // the other ones will call `onUpdate` callback
    if (!this.state.isCreated) {
      this.state.isCreated = true;
      this.options.onCreate(data);
    } else {
      this.options.onUpdate(data);
    }
  }

  /**
   * Helper used to know if the given modifier is enabled.
   * @method
   * @memberof Popper.Utils
   * @returns {Boolean}
   */
  function isModifierEnabled(modifiers, modifierName) {
    return modifiers.some(function (_ref) {
      var name = _ref.name,
          enabled = _ref.enabled;
      return enabled && name === modifierName;
    });
  }

  /**
   * Get the prefixed supported property name
   * @method
   * @memberof Popper.Utils
   * @argument {String} property (camelCase)
   * @returns {String} prefixed property (camelCase or PascalCase, depending on the vendor prefix)
   */
  function getSupportedPropertyName(property) {
    var prefixes = [false, 'ms', 'Webkit', 'Moz', 'O'];
    var upperProp = property.charAt(0).toUpperCase() + property.slice(1);

    for (var i = 0; i < prefixes.length; i++) {
      var prefix = prefixes[i];
      var toCheck = prefix ? '' + prefix + upperProp : property;
      if (typeof document.body.style[toCheck] !== 'undefined') {
        return toCheck;
      }
    }
    return null;
  }

  /**
   * Destroys the popper.
   * @method
   * @memberof Popper
   */
  function destroy() {
    this.state.isDestroyed = true;

    // touch DOM only if `applyStyle` modifier is enabled
    if (isModifierEnabled(this.modifiers, 'applyStyle')) {
      this.popper.removeAttribute('x-placement');
      this.popper.style.position = '';
      this.popper.style.top = '';
      this.popper.style.left = '';
      this.popper.style.right = '';
      this.popper.style.bottom = '';
      this.popper.style.willChange = '';
      this.popper.style[getSupportedPropertyName('transform')] = '';
    }

    this.disableEventListeners();

    // remove the popper if user explicity asked for the deletion on destroy
    // do not use `remove` because IE11 doesn't support it
    if (this.options.removeOnDestroy) {
      this.popper.parentNode.removeChild(this.popper);
    }
    return this;
  }

  /**
   * Get the window associated with the element
   * @argument {Element} element
   * @returns {Window}
   */
  function getWindow(element) {
    var ownerDocument = element.ownerDocument;
    return ownerDocument ? ownerDocument.defaultView : window;
  }

  function attachToScrollParents(scrollParent, event, callback, scrollParents) {
    var isBody = scrollParent.nodeName === 'BODY';
    var target = isBody ? scrollParent.ownerDocument.defaultView : scrollParent;
    target.addEventListener(event, callback, { passive: true });

    if (!isBody) {
      attachToScrollParents(getScrollParent(target.parentNode), event, callback, scrollParents);
    }
    scrollParents.push(target);
  }

  /**
   * Setup needed event listeners used to update the popper position
   * @method
   * @memberof Popper.Utils
   * @private
   */
  function setupEventListeners(reference, options, state, updateBound) {
    // Resize event listener on window
    state.updateBound = updateBound;
    getWindow(reference).addEventListener('resize', state.updateBound, { passive: true });

    // Scroll event listener on scroll parents
    var scrollElement = getScrollParent(reference);
    attachToScrollParents(scrollElement, 'scroll', state.updateBound, state.scrollParents);
    state.scrollElement = scrollElement;
    state.eventsEnabled = true;

    return state;
  }

  /**
   * It will add resize/scroll events and start recalculating
   * position of the popper element when they are triggered.
   * @method
   * @memberof Popper
   */
  function enableEventListeners() {
    if (!this.state.eventsEnabled) {
      this.state = setupEventListeners(this.reference, this.options, this.state, this.scheduleUpdate);
    }
  }

  /**
   * Remove event listeners used to update the popper position
   * @method
   * @memberof Popper.Utils
   * @private
   */
  function removeEventListeners(reference, state) {
    // Remove resize event listener on window
    getWindow(reference).removeEventListener('resize', state.updateBound);

    // Remove scroll event listener on scroll parents
    state.scrollParents.forEach(function (target) {
      target.removeEventListener('scroll', state.updateBound);
    });

    // Reset state
    state.updateBound = null;
    state.scrollParents = [];
    state.scrollElement = null;
    state.eventsEnabled = false;
    return state;
  }

  /**
   * It will remove resize/scroll events and won't recalculate popper position
   * when they are triggered. It also won't trigger `onUpdate` callback anymore,
   * unless you call `update` method manually.
   * @method
   * @memberof Popper
   */
  function disableEventListeners() {
    if (this.state.eventsEnabled) {
      cancelAnimationFrame(this.scheduleUpdate);
      this.state = removeEventListeners(this.reference, this.state);
    }
  }

  /**
   * Tells if a given input is a number
   * @method
   * @memberof Popper.Utils
   * @param {*} input to check
   * @return {Boolean}
   */
  function isNumeric(n) {
    return n !== '' && !isNaN(parseFloat(n)) && isFinite(n);
  }

  /**
   * Set the style to the given popper
   * @method
   * @memberof Popper.Utils
   * @argument {Element} element - Element to apply the style to
   * @argument {Object} styles
   * Object with a list of properties and values which will be applied to the element
   */
  function setStyles(element, styles) {
    Object.keys(styles).forEach(function (prop) {
      var unit = '';
      // add unit if the value is numeric and is one of the following
      if (['width', 'height', 'top', 'right', 'bottom', 'left'].indexOf(prop) !== -1 && isNumeric(styles[prop])) {
        unit = 'px';
      }
      element.style[prop] = styles[prop] + unit;
    });
  }

  /**
   * Set the attributes to the given popper
   * @method
   * @memberof Popper.Utils
   * @argument {Element} element - Element to apply the attributes to
   * @argument {Object} styles
   * Object with a list of properties and values which will be applied to the element
   */
  function setAttributes(element, attributes) {
    Object.keys(attributes).forEach(function (prop) {
      var value = attributes[prop];
      if (value !== false) {
        element.setAttribute(prop, attributes[prop]);
      } else {
        element.removeAttribute(prop);
      }
    });
  }

  /**
   * @function
   * @memberof Modifiers
   * @argument {Object} data - The data object generated by `update` method
   * @argument {Object} data.styles - List of style properties - values to apply to popper element
   * @argument {Object} data.attributes - List of attribute properties - values to apply to popper element
   * @argument {Object} options - Modifiers configuration and options
   * @returns {Object} The same data object
   */
  function applyStyle(data) {
    // any property present in `data.styles` will be applied to the popper,
    // in this way we can make the 3rd party modifiers add custom styles to it
    // Be aware, modifiers could override the properties defined in the previous
    // lines of this modifier!
    setStyles(data.instance.popper, data.styles);

    // any property present in `data.attributes` will be applied to the popper,
    // they will be set as HTML attributes of the element
    setAttributes(data.instance.popper, data.attributes);

    // if arrowElement is defined and arrowStyles has some properties
    if (data.arrowElement && Object.keys(data.arrowStyles).length) {
      setStyles(data.arrowElement, data.arrowStyles);
    }

    return data;
  }

  /**
   * Set the x-placement attribute before everything else because it could be used
   * to add margins to the popper margins needs to be calculated to get the
   * correct popper offsets.
   * @method
   * @memberof Popper.modifiers
   * @param {HTMLElement} reference - The reference element used to position the popper
   * @param {HTMLElement} popper - The HTML element used as popper
   * @param {Object} options - Popper.js options
   */
  function applyStyleOnLoad(reference, popper, options, modifierOptions, state) {
    // compute reference element offsets
    var referenceOffsets = getReferenceOffsets(state, popper, reference, options.positionFixed);

    // compute auto placement, store placement inside the data object,
    // modifiers will be able to edit `placement` if needed
    // and refer to originalPlacement to know the original value
    var placement = computeAutoPlacement(options.placement, referenceOffsets, popper, reference, options.modifiers.flip.boundariesElement, options.modifiers.flip.padding);

    popper.setAttribute('x-placement', placement);

    // Apply `position` to popper before anything else because
    // without the position applied we can't guarantee correct computations
    setStyles(popper, { position: options.positionFixed ? 'fixed' : 'absolute' });

    return options;
  }

  /**
   * @function
   * @memberof Popper.Utils
   * @argument {Object} data - The data object generated by `update` method
   * @argument {Boolean} shouldRound - If the offsets should be rounded at all
   * @returns {Object} The popper's position offsets rounded
   *
   * The tale of pixel-perfect positioning. It's still not 100% perfect, but as
   * good as it can be within reason.
   * Discussion here: https://github.com/FezVrasta/popper.js/pull/715
   *
   * Low DPI screens cause a popper to be blurry if not using full pixels (Safari
   * as well on High DPI screens).
   *
   * Firefox prefers no rounding for positioning and does not have blurriness on
   * high DPI screens.
   *
   * Only horizontal placement and left/right values need to be considered.
   */
  function getRoundedOffsets(data, shouldRound) {
    var _data$offsets = data.offsets,
        popper = _data$offsets.popper,
        reference = _data$offsets.reference;
    var round = Math.round,
        floor = Math.floor;

    var noRound = function noRound(v) {
      return v;
    };

    var referenceWidth = round(reference.width);
    var popperWidth = round(popper.width);

    var isVertical = ['left', 'right'].indexOf(data.placement) !== -1;
    var isVariation = data.placement.indexOf('-') !== -1;
    var sameWidthParity = referenceWidth % 2 === popperWidth % 2;
    var bothOddWidth = referenceWidth % 2 === 1 && popperWidth % 2 === 1;

    var horizontalToInteger = !shouldRound ? noRound : isVertical || isVariation || sameWidthParity ? round : floor;
    var verticalToInteger = !shouldRound ? noRound : round;

    return {
      left: horizontalToInteger(bothOddWidth && !isVariation && shouldRound ? popper.left - 1 : popper.left),
      top: verticalToInteger(popper.top),
      bottom: verticalToInteger(popper.bottom),
      right: horizontalToInteger(popper.right)
    };
  }

  var isFirefox = isBrowser && /Firefox/i.test(navigator.userAgent);

  /**
   * @function
   * @memberof Modifiers
   * @argument {Object} data - The data object generated by `update` method
   * @argument {Object} options - Modifiers configuration and options
   * @returns {Object} The data object, properly modified
   */
  function computeStyle(data, options) {
    var x = options.x,
        y = options.y;
    var popper = data.offsets.popper;

    // Remove this legacy support in Popper.js v2

    var legacyGpuAccelerationOption = find(data.instance.modifiers, function (modifier) {
      return modifier.name === 'applyStyle';
    }).gpuAcceleration;
    if (legacyGpuAccelerationOption !== undefined) {
      console.warn('WARNING: `gpuAcceleration` option moved to `computeStyle` modifier and will not be supported in future versions of Popper.js!');
    }
    var gpuAcceleration = legacyGpuAccelerationOption !== undefined ? legacyGpuAccelerationOption : options.gpuAcceleration;

    var offsetParent = getOffsetParent(data.instance.popper);
    var offsetParentRect = getBoundingClientRect(offsetParent);

    // Styles
    var styles = {
      position: popper.position
    };

    var offsets = getRoundedOffsets(data, window.devicePixelRatio < 2 || !isFirefox);

    var sideA = x === 'bottom' ? 'top' : 'bottom';
    var sideB = y === 'right' ? 'left' : 'right';

    // if gpuAcceleration is set to `true` and transform is supported,
    //  we use `translate3d` to apply the position to the popper we
    // automatically use the supported prefixed version if needed
    var prefixedProperty = getSupportedPropertyName('transform');

    // now, let's make a step back and look at this code closely (wtf?)
    // If the content of the popper grows once it's been positioned, it
    // may happen that the popper gets misplaced because of the new content
    // overflowing its reference element
    // To avoid this problem, we provide two options (x and y), which allow
    // the consumer to define the offset origin.
    // If we position a popper on top of a reference element, we can set
    // `x` to `top` to make the popper grow towards its top instead of
    // its bottom.
    var left = void 0,
        top = void 0;
    if (sideA === 'bottom') {
      // when offsetParent is <html> the positioning is relative to the bottom of the screen (excluding the scrollbar)
      // and not the bottom of the html element
      if (offsetParent.nodeName === 'HTML') {
        top = -offsetParent.clientHeight + offsets.bottom;
      } else {
        top = -offsetParentRect.height + offsets.bottom;
      }
    } else {
      top = offsets.top;
    }
    if (sideB === 'right') {
      if (offsetParent.nodeName === 'HTML') {
        left = -offsetParent.clientWidth + offsets.right;
      } else {
        left = -offsetParentRect.width + offsets.right;
      }
    } else {
      left = offsets.left;
    }
    if (gpuAcceleration && prefixedProperty) {
      styles[prefixedProperty] = 'translate3d(' + left + 'px, ' + top + 'px, 0)';
      styles[sideA] = 0;
      styles[sideB] = 0;
      styles.willChange = 'transform';
    } else {
      // othwerise, we use the standard `top`, `left`, `bottom` and `right` properties
      var invertTop = sideA === 'bottom' ? -1 : 1;
      var invertLeft = sideB === 'right' ? -1 : 1;
      styles[sideA] = top * invertTop;
      styles[sideB] = left * invertLeft;
      styles.willChange = sideA + ', ' + sideB;
    }

    // Attributes
    var attributes = {
      'x-placement': data.placement
    };

    // Update `data` attributes, styles and arrowStyles
    data.attributes = _extends({}, attributes, data.attributes);
    data.styles = _extends({}, styles, data.styles);
    data.arrowStyles = _extends({}, data.offsets.arrow, data.arrowStyles);

    return data;
  }

  /**
   * Helper used to know if the given modifier depends from another one.<br />
   * It checks if the needed modifier is listed and enabled.
   * @method
   * @memberof Popper.Utils
   * @param {Array} modifiers - list of modifiers
   * @param {String} requestingName - name of requesting modifier
   * @param {String} requestedName - name of requested modifier
   * @returns {Boolean}
   */
  function isModifierRequired(modifiers, requestingName, requestedName) {
    var requesting = find(modifiers, function (_ref) {
      var name = _ref.name;
      return name === requestingName;
    });

    var isRequired = !!requesting && modifiers.some(function (modifier) {
      return modifier.name === requestedName && modifier.enabled && modifier.order < requesting.order;
    });

    if (!isRequired) {
      var _requesting = '`' + requestingName + '`';
      var requested = '`' + requestedName + '`';
      console.warn(requested + ' modifier is required by ' + _requesting + ' modifier in order to work, be sure to include it before ' + _requesting + '!');
    }
    return isRequired;
  }

  /**
   * @function
   * @memberof Modifiers
   * @argument {Object} data - The data object generated by update method
   * @argument {Object} options - Modifiers configuration and options
   * @returns {Object} The data object, properly modified
   */
  function arrow(data, options) {
    var _data$offsets$arrow;

    // arrow depends on keepTogether in order to work
    if (!isModifierRequired(data.instance.modifiers, 'arrow', 'keepTogether')) {
      return data;
    }

    var arrowElement = options.element;

    // if arrowElement is a string, suppose it's a CSS selector
    if (typeof arrowElement === 'string') {
      arrowElement = data.instance.popper.querySelector(arrowElement);

      // if arrowElement is not found, don't run the modifier
      if (!arrowElement) {
        return data;
      }
    } else {
      // if the arrowElement isn't a query selector we must check that the
      // provided DOM node is child of its popper node
      if (!data.instance.popper.contains(arrowElement)) {
        console.warn('WARNING: `arrow.element` must be child of its popper element!');
        return data;
      }
    }

    var placement = data.placement.split('-')[0];
    var _data$offsets = data.offsets,
        popper = _data$offsets.popper,
        reference = _data$offsets.reference;

    var isVertical = ['left', 'right'].indexOf(placement) !== -1;

    var len = isVertical ? 'height' : 'width';
    var sideCapitalized = isVertical ? 'Top' : 'Left';
    var side = sideCapitalized.toLowerCase();
    var altSide = isVertical ? 'left' : 'top';
    var opSide = isVertical ? 'bottom' : 'right';
    var arrowElementSize = getOuterSizes(arrowElement)[len];

    //
    // extends keepTogether behavior making sure the popper and its
    // reference have enough pixels in conjunction
    //

    // top/left side
    if (reference[opSide] - arrowElementSize < popper[side]) {
      data.offsets.popper[side] -= popper[side] - (reference[opSide] - arrowElementSize);
    }
    // bottom/right side
    if (reference[side] + arrowElementSize > popper[opSide]) {
      data.offsets.popper[side] += reference[side] + arrowElementSize - popper[opSide];
    }
    data.offsets.popper = getClientRect(data.offsets.popper);

    // compute center of the popper
    var center = reference[side] + reference[len] / 2 - arrowElementSize / 2;

    // Compute the sideValue using the updated popper offsets
    // take popper margin in account because we don't have this info available
    var css = getStyleComputedProperty(data.instance.popper);
    var popperMarginSide = parseFloat(css['margin' + sideCapitalized], 10);
    var popperBorderSide = parseFloat(css['border' + sideCapitalized + 'Width'], 10);
    var sideValue = center - data.offsets.popper[side] - popperMarginSide - popperBorderSide;

    // prevent arrowElement from being placed not contiguously to its popper
    sideValue = Math.max(Math.min(popper[len] - arrowElementSize, sideValue), 0);

    data.arrowElement = arrowElement;
    data.offsets.arrow = (_data$offsets$arrow = {}, defineProperty$1(_data$offsets$arrow, side, Math.round(sideValue)), defineProperty$1(_data$offsets$arrow, altSide, ''), _data$offsets$arrow);

    return data;
  }

  /**
   * Get the opposite placement variation of the given one
   * @method
   * @memberof Popper.Utils
   * @argument {String} placement variation
   * @returns {String} flipped placement variation
   */
  function getOppositeVariation(variation) {
    if (variation === 'end') {
      return 'start';
    } else if (variation === 'start') {
      return 'end';
    }
    return variation;
  }

  /**
   * List of accepted placements to use as values of the `placement` option.<br />
   * Valid placements are:
   * - `auto`
   * - `top`
   * - `right`
   * - `bottom`
   * - `left`
   *
   * Each placement can have a variation from this list:
   * - `-start`
   * - `-end`
   *
   * Variations are interpreted easily if you think of them as the left to right
   * written languages. Horizontally (`top` and `bottom`), `start` is left and `end`
   * is right.<br />
   * Vertically (`left` and `right`), `start` is top and `end` is bottom.
   *
   * Some valid examples are:
   * - `top-end` (on top of reference, right aligned)
   * - `right-start` (on right of reference, top aligned)
   * - `bottom` (on bottom, centered)
   * - `auto-end` (on the side with more space available, alignment depends by placement)
   *
   * @static
   * @type {Array}
   * @enum {String}
   * @readonly
   * @method placements
   * @memberof Popper
   */
  var placements = ['auto-start', 'auto', 'auto-end', 'top-start', 'top', 'top-end', 'right-start', 'right', 'right-end', 'bottom-end', 'bottom', 'bottom-start', 'left-end', 'left', 'left-start'];

  // Get rid of `auto` `auto-start` and `auto-end`
  var validPlacements = placements.slice(3);

  /**
   * Given an initial placement, returns all the subsequent placements
   * clockwise (or counter-clockwise).
   *
   * @method
   * @memberof Popper.Utils
   * @argument {String} placement - A valid placement (it accepts variations)
   * @argument {Boolean} counter - Set to true to walk the placements counterclockwise
   * @returns {Array} placements including their variations
   */
  function clockwise(placement) {
    var counter = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;

    var index = validPlacements.indexOf(placement);
    var arr = validPlacements.slice(index + 1).concat(validPlacements.slice(0, index));
    return counter ? arr.reverse() : arr;
  }

  var BEHAVIORS = {
    FLIP: 'flip',
    CLOCKWISE: 'clockwise',
    COUNTERCLOCKWISE: 'counterclockwise'
  };

  /**
   * @function
   * @memberof Modifiers
   * @argument {Object} data - The data object generated by update method
   * @argument {Object} options - Modifiers configuration and options
   * @returns {Object} The data object, properly modified
   */
  function flip(data, options) {
    // if `inner` modifier is enabled, we can't use the `flip` modifier
    if (isModifierEnabled(data.instance.modifiers, 'inner')) {
      return data;
    }

    if (data.flipped && data.placement === data.originalPlacement) {
      // seems like flip is trying to loop, probably there's not enough space on any of the flippable sides
      return data;
    }

    var boundaries = getBoundaries(data.instance.popper, data.instance.reference, options.padding, options.boundariesElement, data.positionFixed);

    var placement = data.placement.split('-')[0];
    var placementOpposite = getOppositePlacement(placement);
    var variation = data.placement.split('-')[1] || '';

    var flipOrder = [];

    switch (options.behavior) {
      case BEHAVIORS.FLIP:
        flipOrder = [placement, placementOpposite];
        break;
      case BEHAVIORS.CLOCKWISE:
        flipOrder = clockwise(placement);
        break;
      case BEHAVIORS.COUNTERCLOCKWISE:
        flipOrder = clockwise(placement, true);
        break;
      default:
        flipOrder = options.behavior;
    }

    flipOrder.forEach(function (step, index) {
      if (placement !== step || flipOrder.length === index + 1) {
        return data;
      }

      placement = data.placement.split('-')[0];
      placementOpposite = getOppositePlacement(placement);

      var popperOffsets = data.offsets.popper;
      var refOffsets = data.offsets.reference;

      // using floor because the reference offsets may contain decimals we are not going to consider here
      var floor = Math.floor;
      var overlapsRef = placement === 'left' && floor(popperOffsets.right) > floor(refOffsets.left) || placement === 'right' && floor(popperOffsets.left) < floor(refOffsets.right) || placement === 'top' && floor(popperOffsets.bottom) > floor(refOffsets.top) || placement === 'bottom' && floor(popperOffsets.top) < floor(refOffsets.bottom);

      var overflowsLeft = floor(popperOffsets.left) < floor(boundaries.left);
      var overflowsRight = floor(popperOffsets.right) > floor(boundaries.right);
      var overflowsTop = floor(popperOffsets.top) < floor(boundaries.top);
      var overflowsBottom = floor(popperOffsets.bottom) > floor(boundaries.bottom);

      var overflowsBoundaries = placement === 'left' && overflowsLeft || placement === 'right' && overflowsRight || placement === 'top' && overflowsTop || placement === 'bottom' && overflowsBottom;

      // flip the variation if required
      var isVertical = ['top', 'bottom'].indexOf(placement) !== -1;
      var flippedVariation = !!options.flipVariations && (isVertical && variation === 'start' && overflowsLeft || isVertical && variation === 'end' && overflowsRight || !isVertical && variation === 'start' && overflowsTop || !isVertical && variation === 'end' && overflowsBottom);

      if (overlapsRef || overflowsBoundaries || flippedVariation) {
        // this boolean to detect any flip loop
        data.flipped = true;

        if (overlapsRef || overflowsBoundaries) {
          placement = flipOrder[index + 1];
        }

        if (flippedVariation) {
          variation = getOppositeVariation(variation);
        }

        data.placement = placement + (variation ? '-' + variation : '');

        // this object contains `position`, we want to preserve it along with
        // any additional property we may add in the future
        data.offsets.popper = _extends({}, data.offsets.popper, getPopperOffsets(data.instance.popper, data.offsets.reference, data.placement));

        data = runModifiers(data.instance.modifiers, data, 'flip');
      }
    });
    return data;
  }

  /**
   * @function
   * @memberof Modifiers
   * @argument {Object} data - The data object generated by update method
   * @argument {Object} options - Modifiers configuration and options
   * @returns {Object} The data object, properly modified
   */
  function keepTogether(data) {
    var _data$offsets = data.offsets,
        popper = _data$offsets.popper,
        reference = _data$offsets.reference;

    var placement = data.placement.split('-')[0];
    var floor = Math.floor;
    var isVertical = ['top', 'bottom'].indexOf(placement) !== -1;
    var side = isVertical ? 'right' : 'bottom';
    var opSide = isVertical ? 'left' : 'top';
    var measurement = isVertical ? 'width' : 'height';

    if (popper[side] < floor(reference[opSide])) {
      data.offsets.popper[opSide] = floor(reference[opSide]) - popper[measurement];
    }
    if (popper[opSide] > floor(reference[side])) {
      data.offsets.popper[opSide] = floor(reference[side]);
    }

    return data;
  }

  /**
   * Converts a string containing value + unit into a px value number
   * @function
   * @memberof {modifiers~offset}
   * @private
   * @argument {String} str - Value + unit string
   * @argument {String} measurement - `height` or `width`
   * @argument {Object} popperOffsets
   * @argument {Object} referenceOffsets
   * @returns {Number|String}
   * Value in pixels, or original string if no values were extracted
   */
  function toValue(str, measurement, popperOffsets, referenceOffsets) {
    // separate value from unit
    var split = str.match(/((?:\-|\+)?\d*\.?\d*)(.*)/);
    var value = +split[1];
    var unit = split[2];

    // If it's not a number it's an operator, I guess
    if (!value) {
      return str;
    }

    if (unit.indexOf('%') === 0) {
      var element = void 0;
      switch (unit) {
        case '%p':
          element = popperOffsets;
          break;
        case '%':
        case '%r':
        default:
          element = referenceOffsets;
      }

      var rect = getClientRect(element);
      return rect[measurement] / 100 * value;
    } else if (unit === 'vh' || unit === 'vw') {
      // if is a vh or vw, we calculate the size based on the viewport
      var size = void 0;
      if (unit === 'vh') {
        size = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
      } else {
        size = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
      }
      return size / 100 * value;
    } else {
      // if is an explicit pixel unit, we get rid of the unit and keep the value
      // if is an implicit unit, it's px, and we return just the value
      return value;
    }
  }

  /**
   * Parse an `offset` string to extrapolate `x` and `y` numeric offsets.
   * @function
   * @memberof {modifiers~offset}
   * @private
   * @argument {String} offset
   * @argument {Object} popperOffsets
   * @argument {Object} referenceOffsets
   * @argument {String} basePlacement
   * @returns {Array} a two cells array with x and y offsets in numbers
   */
  function parseOffset(offset, popperOffsets, referenceOffsets, basePlacement) {
    var offsets = [0, 0];

    // Use height if placement is left or right and index is 0 otherwise use width
    // in this way the first offset will use an axis and the second one
    // will use the other one
    var useHeight = ['right', 'left'].indexOf(basePlacement) !== -1;

    // Split the offset string to obtain a list of values and operands
    // The regex addresses values with the plus or minus sign in front (+10, -20, etc)
    var fragments = offset.split(/(\+|\-)/).map(function (frag) {
      return frag.trim();
    });

    // Detect if the offset string contains a pair of values or a single one
    // they could be separated by comma or space
    var divider = fragments.indexOf(find(fragments, function (frag) {
      return frag.search(/,|\s/) !== -1;
    }));

    if (fragments[divider] && fragments[divider].indexOf(',') === -1) {
      console.warn('Offsets separated by white space(s) are deprecated, use a comma (,) instead.');
    }

    // If divider is found, we divide the list of values and operands to divide
    // them by ofset X and Y.
    var splitRegex = /\s*,\s*|\s+/;
    var ops = divider !== -1 ? [fragments.slice(0, divider).concat([fragments[divider].split(splitRegex)[0]]), [fragments[divider].split(splitRegex)[1]].concat(fragments.slice(divider + 1))] : [fragments];

    // Convert the values with units to absolute pixels to allow our computations
    ops = ops.map(function (op, index) {
      // Most of the units rely on the orientation of the popper
      var measurement = (index === 1 ? !useHeight : useHeight) ? 'height' : 'width';
      var mergeWithPrevious = false;
      return op
      // This aggregates any `+` or `-` sign that aren't considered operators
      // e.g.: 10 + +5 => [10, +, +5]
      .reduce(function (a, b) {
        if (a[a.length - 1] === '' && ['+', '-'].indexOf(b) !== -1) {
          a[a.length - 1] = b;
          mergeWithPrevious = true;
          return a;
        } else if (mergeWithPrevious) {
          a[a.length - 1] += b;
          mergeWithPrevious = false;
          return a;
        } else {
          return a.concat(b);
        }
      }, [])
      // Here we convert the string values into number values (in px)
      .map(function (str) {
        return toValue(str, measurement, popperOffsets, referenceOffsets);
      });
    });

    // Loop trough the offsets arrays and execute the operations
    ops.forEach(function (op, index) {
      op.forEach(function (frag, index2) {
        if (isNumeric(frag)) {
          offsets[index] += frag * (op[index2 - 1] === '-' ? -1 : 1);
        }
      });
    });
    return offsets;
  }

  /**
   * @function
   * @memberof Modifiers
   * @argument {Object} data - The data object generated by update method
   * @argument {Object} options - Modifiers configuration and options
   * @argument {Number|String} options.offset=0
   * The offset value as described in the modifier description
   * @returns {Object} The data object, properly modified
   */
  function offset$1(data, _ref) {
    var offset = _ref.offset;
    var placement = data.placement,
        _data$offsets = data.offsets,
        popper = _data$offsets.popper,
        reference = _data$offsets.reference;

    var basePlacement = placement.split('-')[0];

    var offsets = void 0;
    if (isNumeric(+offset)) {
      offsets = [+offset, 0];
    } else {
      offsets = parseOffset(offset, popper, reference, basePlacement);
    }

    if (basePlacement === 'left') {
      popper.top += offsets[0];
      popper.left -= offsets[1];
    } else if (basePlacement === 'right') {
      popper.top += offsets[0];
      popper.left += offsets[1];
    } else if (basePlacement === 'top') {
      popper.left += offsets[0];
      popper.top -= offsets[1];
    } else if (basePlacement === 'bottom') {
      popper.left += offsets[0];
      popper.top += offsets[1];
    }

    data.popper = popper;
    return data;
  }

  /**
   * @function
   * @memberof Modifiers
   * @argument {Object} data - The data object generated by `update` method
   * @argument {Object} options - Modifiers configuration and options
   * @returns {Object} The data object, properly modified
   */
  function preventOverflow(data, options) {
    var boundariesElement = options.boundariesElement || getOffsetParent(data.instance.popper);

    // If offsetParent is the reference element, we really want to
    // go one step up and use the next offsetParent as reference to
    // avoid to make this modifier completely useless and look like broken
    if (data.instance.reference === boundariesElement) {
      boundariesElement = getOffsetParent(boundariesElement);
    }

    // NOTE: DOM access here
    // resets the popper's position so that the document size can be calculated excluding
    // the size of the popper element itself
    var transformProp = getSupportedPropertyName('transform');
    var popperStyles = data.instance.popper.style; // assignment to help minification
    var top = popperStyles.top,
        left = popperStyles.left,
        transform = popperStyles[transformProp];

    popperStyles.top = '';
    popperStyles.left = '';
    popperStyles[transformProp] = '';

    var boundaries = getBoundaries(data.instance.popper, data.instance.reference, options.padding, boundariesElement, data.positionFixed);

    // NOTE: DOM access here
    // restores the original style properties after the offsets have been computed
    popperStyles.top = top;
    popperStyles.left = left;
    popperStyles[transformProp] = transform;

    options.boundaries = boundaries;

    var order = options.priority;
    var popper = data.offsets.popper;

    var check = {
      primary: function primary(placement) {
        var value = popper[placement];
        if (popper[placement] < boundaries[placement] && !options.escapeWithReference) {
          value = Math.max(popper[placement], boundaries[placement]);
        }
        return defineProperty$1({}, placement, value);
      },
      secondary: function secondary(placement) {
        var mainSide = placement === 'right' ? 'left' : 'top';
        var value = popper[mainSide];
        if (popper[placement] > boundaries[placement] && !options.escapeWithReference) {
          value = Math.min(popper[mainSide], boundaries[placement] - (placement === 'right' ? popper.width : popper.height));
        }
        return defineProperty$1({}, mainSide, value);
      }
    };

    order.forEach(function (placement) {
      var side = ['left', 'top'].indexOf(placement) !== -1 ? 'primary' : 'secondary';
      popper = _extends({}, popper, check[side](placement));
    });

    data.offsets.popper = popper;

    return data;
  }

  /**
   * @function
   * @memberof Modifiers
   * @argument {Object} data - The data object generated by `update` method
   * @argument {Object} options - Modifiers configuration and options
   * @returns {Object} The data object, properly modified
   */
  function shift(data) {
    var placement = data.placement;
    var basePlacement = placement.split('-')[0];
    var shiftvariation = placement.split('-')[1];

    // if shift shiftvariation is specified, run the modifier
    if (shiftvariation) {
      var _data$offsets = data.offsets,
          reference = _data$offsets.reference,
          popper = _data$offsets.popper;

      var isVertical = ['bottom', 'top'].indexOf(basePlacement) !== -1;
      var side = isVertical ? 'left' : 'top';
      var measurement = isVertical ? 'width' : 'height';

      var shiftOffsets = {
        start: defineProperty$1({}, side, reference[side]),
        end: defineProperty$1({}, side, reference[side] + reference[measurement] - popper[measurement])
      };

      data.offsets.popper = _extends({}, popper, shiftOffsets[shiftvariation]);
    }

    return data;
  }

  /**
   * @function
   * @memberof Modifiers
   * @argument {Object} data - The data object generated by update method
   * @argument {Object} options - Modifiers configuration and options
   * @returns {Object} The data object, properly modified
   */
  function hide(data) {
    if (!isModifierRequired(data.instance.modifiers, 'hide', 'preventOverflow')) {
      return data;
    }

    var refRect = data.offsets.reference;
    var bound = find(data.instance.modifiers, function (modifier) {
      return modifier.name === 'preventOverflow';
    }).boundaries;

    if (refRect.bottom < bound.top || refRect.left > bound.right || refRect.top > bound.bottom || refRect.right < bound.left) {
      // Avoid unnecessary DOM access if visibility hasn't changed
      if (data.hide === true) {
        return data;
      }

      data.hide = true;
      data.attributes['x-out-of-boundaries'] = '';
    } else {
      // Avoid unnecessary DOM access if visibility hasn't changed
      if (data.hide === false) {
        return data;
      }

      data.hide = false;
      data.attributes['x-out-of-boundaries'] = false;
    }

    return data;
  }

  /**
   * @function
   * @memberof Modifiers
   * @argument {Object} data - The data object generated by `update` method
   * @argument {Object} options - Modifiers configuration and options
   * @returns {Object} The data object, properly modified
   */
  function inner(data) {
    var placement = data.placement;
    var basePlacement = placement.split('-')[0];
    var _data$offsets = data.offsets,
        popper = _data$offsets.popper,
        reference = _data$offsets.reference;

    var isHoriz = ['left', 'right'].indexOf(basePlacement) !== -1;

    var subtractLength = ['top', 'left'].indexOf(basePlacement) === -1;

    popper[isHoriz ? 'left' : 'top'] = reference[basePlacement] - (subtractLength ? popper[isHoriz ? 'width' : 'height'] : 0);

    data.placement = getOppositePlacement(placement);
    data.offsets.popper = getClientRect(popper);

    return data;
  }

  /**
   * Modifier function, each modifier can have a function of this type assigned
   * to its `fn` property.<br />
   * These functions will be called on each update, this means that you must
   * make sure they are performant enough to avoid performance bottlenecks.
   *
   * @function ModifierFn
   * @argument {dataObject} data - The data object generated by `update` method
   * @argument {Object} options - Modifiers configuration and options
   * @returns {dataObject} The data object, properly modified
   */

  /**
   * Modifiers are plugins used to alter the behavior of your poppers.<br />
   * Popper.js uses a set of 9 modifiers to provide all the basic functionalities
   * needed by the library.
   *
   * Usually you don't want to override the `order`, `fn` and `onLoad` props.
   * All the other properties are configurations that could be tweaked.
   * @namespace modifiers
   */
  var modifiers = {
    /**
     * Modifier used to shift the popper on the start or end of its reference
     * element.<br />
     * It will read the variation of the `placement` property.<br />
     * It can be one either `-end` or `-start`.
     * @memberof modifiers
     * @inner
     */
    shift: {
      /** @prop {number} order=100 - Index used to define the order of execution */
      order: 100,
      /** @prop {Boolean} enabled=true - Whether the modifier is enabled or not */
      enabled: true,
      /** @prop {ModifierFn} */
      fn: shift
    },

    /**
     * The `offset` modifier can shift your popper on both its axis.
     *
     * It accepts the following units:
     * - `px` or unit-less, interpreted as pixels
     * - `%` or `%r`, percentage relative to the length of the reference element
     * - `%p`, percentage relative to the length of the popper element
     * - `vw`, CSS viewport width unit
     * - `vh`, CSS viewport height unit
     *
     * For length is intended the main axis relative to the placement of the popper.<br />
     * This means that if the placement is `top` or `bottom`, the length will be the
     * `width`. In case of `left` or `right`, it will be the `height`.
     *
     * You can provide a single value (as `Number` or `String`), or a pair of values
     * as `String` divided by a comma or one (or more) white spaces.<br />
     * The latter is a deprecated method because it leads to confusion and will be
     * removed in v2.<br />
     * Additionally, it accepts additions and subtractions between different units.
     * Note that multiplications and divisions aren't supported.
     *
     * Valid examples are:
     * ```
     * 10
     * '10%'
     * '10, 10'
     * '10%, 10'
     * '10 + 10%'
     * '10 - 5vh + 3%'
     * '-10px + 5vh, 5px - 6%'
     * ```
     * > **NB**: If you desire to apply offsets to your poppers in a way that may make them overlap
     * > with their reference element, unfortunately, you will have to disable the `flip` modifier.
     * > You can read more on this at this [issue](https://github.com/FezVrasta/popper.js/issues/373).
     *
     * @memberof modifiers
     * @inner
     */
    offset: {
      /** @prop {number} order=200 - Index used to define the order of execution */
      order: 200,
      /** @prop {Boolean} enabled=true - Whether the modifier is enabled or not */
      enabled: true,
      /** @prop {ModifierFn} */
      fn: offset$1,
      /** @prop {Number|String} offset=0
       * The offset value as described in the modifier description
       */
      offset: 0
    },

    /**
     * Modifier used to prevent the popper from being positioned outside the boundary.
     *
     * A scenario exists where the reference itself is not within the boundaries.<br />
     * We can say it has "escaped the boundaries" — or just "escaped".<br />
     * In this case we need to decide whether the popper should either:
     *
     * - detach from the reference and remain "trapped" in the boundaries, or
     * - if it should ignore the boundary and "escape with its reference"
     *
     * When `escapeWithReference` is set to`true` and reference is completely
     * outside its boundaries, the popper will overflow (or completely leave)
     * the boundaries in order to remain attached to the edge of the reference.
     *
     * @memberof modifiers
     * @inner
     */
    preventOverflow: {
      /** @prop {number} order=300 - Index used to define the order of execution */
      order: 300,
      /** @prop {Boolean} enabled=true - Whether the modifier is enabled or not */
      enabled: true,
      /** @prop {ModifierFn} */
      fn: preventOverflow,
      /**
       * @prop {Array} [priority=['left','right','top','bottom']]
       * Popper will try to prevent overflow following these priorities by default,
       * then, it could overflow on the left and on top of the `boundariesElement`
       */
      priority: ['left', 'right', 'top', 'bottom'],
      /**
       * @prop {number} padding=5
       * Amount of pixel used to define a minimum distance between the boundaries
       * and the popper. This makes sure the popper always has a little padding
       * between the edges of its container
       */
      padding: 5,
      /**
       * @prop {String|HTMLElement} boundariesElement='scrollParent'
       * Boundaries used by the modifier. Can be `scrollParent`, `window`,
       * `viewport` or any DOM element.
       */
      boundariesElement: 'scrollParent'
    },

    /**
     * Modifier used to make sure the reference and its popper stay near each other
     * without leaving any gap between the two. Especially useful when the arrow is
     * enabled and you want to ensure that it points to its reference element.
     * It cares only about the first axis. You can still have poppers with margin
     * between the popper and its reference element.
     * @memberof modifiers
     * @inner
     */
    keepTogether: {
      /** @prop {number} order=400 - Index used to define the order of execution */
      order: 400,
      /** @prop {Boolean} enabled=true - Whether the modifier is enabled or not */
      enabled: true,
      /** @prop {ModifierFn} */
      fn: keepTogether
    },

    /**
     * This modifier is used to move the `arrowElement` of the popper to make
     * sure it is positioned between the reference element and its popper element.
     * It will read the outer size of the `arrowElement` node to detect how many
     * pixels of conjunction are needed.
     *
     * It has no effect if no `arrowElement` is provided.
     * @memberof modifiers
     * @inner
     */
    arrow: {
      /** @prop {number} order=500 - Index used to define the order of execution */
      order: 500,
      /** @prop {Boolean} enabled=true - Whether the modifier is enabled or not */
      enabled: true,
      /** @prop {ModifierFn} */
      fn: arrow,
      /** @prop {String|HTMLElement} element='[x-arrow]' - Selector or node used as arrow */
      element: '[x-arrow]'
    },

    /**
     * Modifier used to flip the popper's placement when it starts to overlap its
     * reference element.
     *
     * Requires the `preventOverflow` modifier before it in order to work.
     *
     * **NOTE:** this modifier will interrupt the current update cycle and will
     * restart it if it detects the need to flip the placement.
     * @memberof modifiers
     * @inner
     */
    flip: {
      /** @prop {number} order=600 - Index used to define the order of execution */
      order: 600,
      /** @prop {Boolean} enabled=true - Whether the modifier is enabled or not */
      enabled: true,
      /** @prop {ModifierFn} */
      fn: flip,
      /**
       * @prop {String|Array} behavior='flip'
       * The behavior used to change the popper's placement. It can be one of
       * `flip`, `clockwise`, `counterclockwise` or an array with a list of valid
       * placements (with optional variations)
       */
      behavior: 'flip',
      /**
       * @prop {number} padding=5
       * The popper will flip if it hits the edges of the `boundariesElement`
       */
      padding: 5,
      /**
       * @prop {String|HTMLElement} boundariesElement='viewport'
       * The element which will define the boundaries of the popper position.
       * The popper will never be placed outside of the defined boundaries
       * (except if `keepTogether` is enabled)
       */
      boundariesElement: 'viewport'
    },

    /**
     * Modifier used to make the popper flow toward the inner of the reference element.
     * By default, when this modifier is disabled, the popper will be placed outside
     * the reference element.
     * @memberof modifiers
     * @inner
     */
    inner: {
      /** @prop {number} order=700 - Index used to define the order of execution */
      order: 700,
      /** @prop {Boolean} enabled=false - Whether the modifier is enabled or not */
      enabled: false,
      /** @prop {ModifierFn} */
      fn: inner
    },

    /**
     * Modifier used to hide the popper when its reference element is outside of the
     * popper boundaries. It will set a `x-out-of-boundaries` attribute which can
     * be used to hide with a CSS selector the popper when its reference is
     * out of boundaries.
     *
     * Requires the `preventOverflow` modifier before it in order to work.
     * @memberof modifiers
     * @inner
     */
    hide: {
      /** @prop {number} order=800 - Index used to define the order of execution */
      order: 800,
      /** @prop {Boolean} enabled=true - Whether the modifier is enabled or not */
      enabled: true,
      /** @prop {ModifierFn} */
      fn: hide
    },

    /**
     * Computes the style that will be applied to the popper element to gets
     * properly positioned.
     *
     * Note that this modifier will not touch the DOM, it just prepares the styles
     * so that `applyStyle` modifier can apply it. This separation is useful
     * in case you need to replace `applyStyle` with a custom implementation.
     *
     * This modifier has `850` as `order` value to maintain backward compatibility
     * with previous versions of Popper.js. Expect the modifiers ordering method
     * to change in future major versions of the library.
     *
     * @memberof modifiers
     * @inner
     */
    computeStyle: {
      /** @prop {number} order=850 - Index used to define the order of execution */
      order: 850,
      /** @prop {Boolean} enabled=true - Whether the modifier is enabled or not */
      enabled: true,
      /** @prop {ModifierFn} */
      fn: computeStyle,
      /**
       * @prop {Boolean} gpuAcceleration=true
       * If true, it uses the CSS 3D transformation to position the popper.
       * Otherwise, it will use the `top` and `left` properties
       */
      gpuAcceleration: true,
      /**
       * @prop {string} [x='bottom']
       * Where to anchor the X axis (`bottom` or `top`). AKA X offset origin.
       * Change this if your popper should grow in a direction different from `bottom`
       */
      x: 'bottom',
      /**
       * @prop {string} [x='left']
       * Where to anchor the Y axis (`left` or `right`). AKA Y offset origin.
       * Change this if your popper should grow in a direction different from `right`
       */
      y: 'right'
    },

    /**
     * Applies the computed styles to the popper element.
     *
     * All the DOM manipulations are limited to this modifier. This is useful in case
     * you want to integrate Popper.js inside a framework or view library and you
     * want to delegate all the DOM manipulations to it.
     *
     * Note that if you disable this modifier, you must make sure the popper element
     * has its position set to `absolute` before Popper.js can do its work!
     *
     * Just disable this modifier and define your own to achieve the desired effect.
     *
     * @memberof modifiers
     * @inner
     */
    applyStyle: {
      /** @prop {number} order=900 - Index used to define the order of execution */
      order: 900,
      /** @prop {Boolean} enabled=true - Whether the modifier is enabled or not */
      enabled: true,
      /** @prop {ModifierFn} */
      fn: applyStyle,
      /** @prop {Function} */
      onLoad: applyStyleOnLoad,
      /**
       * @deprecated since version 1.10.0, the property moved to `computeStyle` modifier
       * @prop {Boolean} gpuAcceleration=true
       * If true, it uses the CSS 3D transformation to position the popper.
       * Otherwise, it will use the `top` and `left` properties
       */
      gpuAcceleration: undefined
    }
  };

  /**
   * The `dataObject` is an object containing all the information used by Popper.js.
   * This object is passed to modifiers and to the `onCreate` and `onUpdate` callbacks.
   * @name dataObject
   * @property {Object} data.instance The Popper.js instance
   * @property {String} data.placement Placement applied to popper
   * @property {String} data.originalPlacement Placement originally defined on init
   * @property {Boolean} data.flipped True if popper has been flipped by flip modifier
   * @property {Boolean} data.hide True if the reference element is out of boundaries, useful to know when to hide the popper
   * @property {HTMLElement} data.arrowElement Node used as arrow by arrow modifier
   * @property {Object} data.styles Any CSS property defined here will be applied to the popper. It expects the JavaScript nomenclature (eg. `marginBottom`)
   * @property {Object} data.arrowStyles Any CSS property defined here will be applied to the popper arrow. It expects the JavaScript nomenclature (eg. `marginBottom`)
   * @property {Object} data.boundaries Offsets of the popper boundaries
   * @property {Object} data.offsets The measurements of popper, reference and arrow elements
   * @property {Object} data.offsets.popper `top`, `left`, `width`, `height` values
   * @property {Object} data.offsets.reference `top`, `left`, `width`, `height` values
   * @property {Object} data.offsets.arrow] `top` and `left` offsets, only one of them will be different from 0
   */

  /**
   * Default options provided to Popper.js constructor.<br />
   * These can be overridden using the `options` argument of Popper.js.<br />
   * To override an option, simply pass an object with the same
   * structure of the `options` object, as the 3rd argument. For example:
   * ```
   * new Popper(ref, pop, {
   *   modifiers: {
   *     preventOverflow: { enabled: false }
   *   }
   * })
   * ```
   * @type {Object}
   * @static
   * @memberof Popper
   */
  var Defaults = {
    /**
     * Popper's placement.
     * @prop {Popper.placements} placement='bottom'
     */
    placement: 'bottom',

    /**
     * Set this to true if you want popper to position it self in 'fixed' mode
     * @prop {Boolean} positionFixed=false
     */
    positionFixed: false,

    /**
     * Whether events (resize, scroll) are initially enabled.
     * @prop {Boolean} eventsEnabled=true
     */
    eventsEnabled: true,

    /**
     * Set to true if you want to automatically remove the popper when
     * you call the `destroy` method.
     * @prop {Boolean} removeOnDestroy=false
     */
    removeOnDestroy: false,

    /**
     * Callback called when the popper is created.<br />
     * By default, it is set to no-op.<br />
     * Access Popper.js instance with `data.instance`.
     * @prop {onCreate}
     */
    onCreate: function onCreate() {},

    /**
     * Callback called when the popper is updated. This callback is not called
     * on the initialization/creation of the popper, but only on subsequent
     * updates.<br />
     * By default, it is set to no-op.<br />
     * Access Popper.js instance with `data.instance`.
     * @prop {onUpdate}
     */
    onUpdate: function onUpdate() {},

    /**
     * List of modifiers used to modify the offsets before they are applied to the popper.
     * They provide most of the functionalities of Popper.js.
     * @prop {modifiers}
     */
    modifiers: modifiers
  };

  /**
   * @callback onCreate
   * @param {dataObject} data
   */

  /**
   * @callback onUpdate
   * @param {dataObject} data
   */

  // Utils
  // Methods
  var Popper = function () {
    /**
     * Creates a new Popper.js instance.
     * @class Popper
     * @param {HTMLElement|referenceObject} reference - The reference element used to position the popper
     * @param {HTMLElement} popper - The HTML element used as the popper
     * @param {Object} options - Your custom options to override the ones defined in [Defaults](#defaults)
     * @return {Object} instance - The generated Popper.js instance
     */
    function Popper(reference, popper) {
      var _this = this;

      var options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
      classCallCheck(this, Popper);

      this.scheduleUpdate = function () {
        return requestAnimationFrame(_this.update);
      };

      // make update() debounced, so that it only runs at most once-per-tick
      this.update = debounce(this.update.bind(this));

      // with {} we create a new object with the options inside it
      this.options = _extends({}, Popper.Defaults, options);

      // init state
      this.state = {
        isDestroyed: false,
        isCreated: false,
        scrollParents: []
      };

      // get reference and popper elements (allow jQuery wrappers)
      this.reference = reference && reference.jquery ? reference[0] : reference;
      this.popper = popper && popper.jquery ? popper[0] : popper;

      // Deep merge modifiers options
      this.options.modifiers = {};
      Object.keys(_extends({}, Popper.Defaults.modifiers, options.modifiers)).forEach(function (name) {
        _this.options.modifiers[name] = _extends({}, Popper.Defaults.modifiers[name] || {}, options.modifiers ? options.modifiers[name] : {});
      });

      // Refactoring modifiers' list (Object => Array)
      this.modifiers = Object.keys(this.options.modifiers).map(function (name) {
        return _extends({
          name: name
        }, _this.options.modifiers[name]);
      })
      // sort the modifiers by order
      .sort(function (a, b) {
        return a.order - b.order;
      });

      // modifiers have the ability to execute arbitrary code when Popper.js get inited
      // such code is executed in the same order of its modifier
      // they could add new properties to their options configuration
      // BE AWARE: don't add options to `options.modifiers.name` but to `modifierOptions`!
      this.modifiers.forEach(function (modifierOptions) {
        if (modifierOptions.enabled && isFunction(modifierOptions.onLoad)) {
          modifierOptions.onLoad(_this.reference, _this.popper, _this.options, modifierOptions, _this.state);
        }
      });

      // fire the first update to position the popper in the right place
      this.update();

      var eventsEnabled = this.options.eventsEnabled;
      if (eventsEnabled) {
        // setup event listeners, they will take care of update the position in specific situations
        this.enableEventListeners();
      }

      this.state.eventsEnabled = eventsEnabled;
    }

    // We can't use class properties because they don't get listed in the
    // class prototype and break stuff like Sinon stubs


    createClass(Popper, [{
      key: 'update',
      value: function update$$1() {
        return update.call(this);
      }
    }, {
      key: 'destroy',
      value: function destroy$$1() {
        return destroy.call(this);
      }
    }, {
      key: 'enableEventListeners',
      value: function enableEventListeners$$1() {
        return enableEventListeners.call(this);
      }
    }, {
      key: 'disableEventListeners',
      value: function disableEventListeners$$1() {
        return disableEventListeners.call(this);
      }

      /**
       * Schedules an update. It will run on the next UI update available.
       * @method scheduleUpdate
       * @memberof Popper
       */


      /**
       * Collection of utilities useful when writing custom modifiers.
       * Starting from version 1.7, this method is available only if you
       * include `popper-utils.js` before `popper.js`.
       *
       * **DEPRECATION**: This way to access PopperUtils is deprecated
       * and will be removed in v2! Use the PopperUtils module directly instead.
       * Due to the high instability of the methods contained in Utils, we can't
       * guarantee them to follow semver. Use them at your own risk!
       * @static
       * @private
       * @type {Object}
       * @deprecated since version 1.8
       * @member Utils
       * @memberof Popper
       */

    }]);
    return Popper;
  }();

  /**
   * The `referenceObject` is an object that provides an interface compatible with Popper.js
   * and lets you use it as replacement of a real DOM node.<br />
   * You can use this method to position a popper relatively to a set of coordinates
   * in case you don't have a DOM node to use as reference.
   *
   * ```
   * new Popper(referenceObject, popperNode);
   * ```
   *
   * NB: This feature isn't supported in Internet Explorer 10.
   * @name referenceObject
   * @property {Function} data.getBoundingClientRect
   * A function that returns a set of coordinates compatible with the native `getBoundingClientRect` method.
   * @property {number} data.clientWidth
   * An ES6 getter that will return the width of the virtual reference element.
   * @property {number} data.clientHeight
   * An ES6 getter that will return the height of the virtual reference element.
   */


  Popper.Utils = (typeof window !== 'undefined' ? window : global).PopperUtils;
  Popper.placements = placements;
  Popper.Defaults = Defaults;

  var clickOutMixin = {
    data: function data() {
      return {
        listenForClickOut: false
      };
    },
    watch: {
      listenForClickOut: function listenForClickOut(newValue, oldValue) {
        if (newValue !== oldValue) {
          eventOff(this.clickOutElement, this.clickOutEventName, this._clickOutHandler, false);

          if (newValue) {
            eventOn(this.clickOutElement, this.clickOutEventName, this._clickOutHandler, false);
          }
        }
      }
    },
    beforeCreate: function beforeCreate() {
      // Declare non-reactive properties
      this.clickOutElement = null;
      this.clickOutEventName = null;
    },
    mounted: function mounted() {
      if (!this.clickOutElement) {
        this.clickOutElement = document;
      }

      if (!this.clickOutEventName) {
        this.clickOutEventName = 'ontouchstart' in document.documentElement ? 'touchstart' : 'click';
      }

      if (this.listenForClickOut) {
        eventOn(this.clickOutElement, this.clickOutEventName, this._clickOutHandler, false);
      }
    },
    beforeDestroy: function beforeDestroy() {
      eventOff(this.clickOutElement, this.clickOutEventName, this._clickOutHandler, false);
    },
    methods: {
      isClickOut: function isClickOut(evt) {
        return !contains(this.$el, evt.target);
      },
      _clickOutHandler: function _clickOutHandler(evt) {
        if (this.clickOutHandler && this.isClickOut(evt)) {
          this.clickOutHandler(evt);
        }
      }
    }
  };

  var focusInMixin = {
    data: function data() {
      return {
        listenForFocusIn: false
      };
    },
    watch: {
      listenForFocusIn: function listenForFocusIn(newValue, oldValue) {
        if (newValue !== oldValue) {
          eventOff(this.focusInElement, 'focusin', this._focusInHandler, false);

          if (newValue) {
            eventOn(this.focusInElement, 'focusin', this._focusInHandler, false);
          }
        }
      }
    },
    beforeCreate: function beforeCreate() {
      // Declare non-reactive properties
      this.focusInElement = null;
    },
    mounted: function mounted() {
      if (!this.focusInElement) {
        this.focusInElement = document;
      }

      if (this.listenForFocusIn) {
        eventOn(this.focusInElement, 'focusin', this._focusInHandler, false);
      }
    },
    beforeDestroy: function beforeDestroy() {
      eventOff(this.focusInElement, 'focusin', this._focusInHandler, false);
    },
    methods: {
      _focusInHandler: function _focusInHandler(evt) {
        if (this.focusInHandler) {
          this.focusInHandler(evt);
        }
      }
    }
  };

  var BvEvent =
  /*#__PURE__*/
  function () {
    function BvEvent(type) {
      var eventInit = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

      _classCallCheck(this, BvEvent);

      // Start by emulating native Event constructor.
      if (!type) {
        throw new TypeError("Failed to construct '".concat(this.constructor.name, "'. 1 argument required, ").concat(arguments.length, " given."));
      } // Assign defaults first, the eventInit,
      // and the type last so it can't be overwritten.


      assign(this, BvEvent.defaults(), eventInit, {
        type: type
      }); // Freeze some props as readonly, but leave them enumerable.

      defineProperties(this, {
        type: readonlyDescriptor(),
        cancelable: readonlyDescriptor(),
        nativeEvent: readonlyDescriptor(),
        target: readonlyDescriptor(),
        relatedTarget: readonlyDescriptor(),
        vueTarget: readonlyDescriptor()
      }); // Create a private variable using closure scoping.

      var defaultPrevented = false; // Recreate preventDefault method. One way setter.

      this.preventDefault = function preventDefault() {
        if (this.cancelable) {
          defaultPrevented = true;
        }
      }; // Create 'defaultPrevented' publicly accessible prop
      // that can only be altered by the preventDefault method.


      defineProperty(this, 'defaultPrevented', {
        enumerable: true,
        get: function get() {
          return defaultPrevented;
        }
      });
    }

    _createClass(BvEvent, null, [{
      key: "defaults",
      value: function defaults() {
        return {
          type: '',
          cancelable: true,
          nativeEvent: null,
          target: null,
          relatedTarget: null,
          vueTarget: null
        };
      }
    }]);

    return BvEvent;
  }();

  /**
   * Log a warning message to the console with bootstrap-vue formatting sugar.
   * @param {string} message
   */

  /* istanbul ignore next */
  function warn(message) {
    console.warn("[BootstrapVue warn]: ".concat(message));
  }

  function filterVisible(els) {
    return (els || []).filter(isVisible);
  } // Dropdown item CSS selectors
  // TODO: .dropdown-form handling


  var Selector = {
    FORM_CHILD: '.dropdown form',
    NAVBAR_NAV: '.navbar-nav',
    ITEM_SELECTOR: '.dropdown-item:not(.disabled):not([disabled])' // Popper attachment positions

  };
  var AttachmentMap = {
    // Dropup left align
    TOP: 'top-start',
    // Dropup right align
    TOPEND: 'top-end',
    // Dropdown left align
    BOTTOM: 'bottom-start',
    // Dropdown right align
    BOTTOMEND: 'bottom-end',
    // Dropright left align
    RIGHT: 'right-start',
    // Dropright right align
    RIGHTEND: 'right-end',
    // Dropleft left align
    LEFT: 'left-start',
    // Dropleft right align
    LEFTEND: 'left-end' // @vue/component

  };
  var dropdownMixin = {
    mixins: [clickOutMixin, focusInMixin],
    provide: function provide() {
      return {
        dropdown: this
      };
    },
    props: {
      disabled: {
        type: Boolean,
        default: false
      },
      text: {
        // Button label
        type: String,
        default: ''
      },
      html: {
        // Button label
        type: String
      },
      dropup: {
        // place on top if possible
        type: Boolean,
        default: false
      },
      dropright: {
        // place right if possible
        type: Boolean,
        default: false
      },
      dropleft: {
        // place left if possible
        type: Boolean,
        default: false
      },
      right: {
        // Right align menu (default is left align)
        type: Boolean,
        default: false
      },
      offset: {
        // Number of pixels to offset menu, or a CSS unit value (i.e. 1px, 1rem, etc)
        type: [Number, String],
        default: 0
      },
      noFlip: {
        // Disable auto-flipping of menu from bottom<=>top
        type: Boolean,
        default: false
      },
      popperOpts: {
        // type: Object,
        default: function _default() {}
      }
    },
    data: function data() {
      return {
        visible: false,
        inNavbar: null,
        visibleChangePrevented: false
      };
    },
    computed: {
      toggler: function toggler() {
        var toggle = this.$refs.toggle;
        return toggle ? toggle.$el || toggle : null;
      }
    },
    watch: {
      visible: function visible(newValue, oldValue) {
        if (this.visibleChangePrevented) {
          this.visibleChangePrevented = false;
          return;
        }

        if (newValue !== oldValue) {
          var evtName = newValue ? 'show' : 'hide';
          var bvEvt = new BvEvent(evtName, {
            cancelable: true,
            vueTarget: this,
            target: this.$refs.menu,
            relatedTarget: null
          });
          this.emitEvent(bvEvt);

          if (bvEvt.defaultPrevented) {
            // Reset value and exit if canceled
            this.visibleChangePrevented = true;
            this.visible = oldValue; // Just in case a child element triggereded this.hide(true)

            this.$off('hidden', this.focusToggler);
            return;
          }

          if (evtName === 'show') {
            this.showMenu();
          } else {
            this.hideMenu();
          }
        }
      },
      disabled: function disabled(newValue, oldValue) {
        if (newValue !== oldValue && newValue && this.visible) {
          // Hide dropdown if disabled changes to true
          this.visible = false;
        }
      }
    },
    created: function created() {
      // Create non-reactive property
      this._popper = null;
    },
    deactivated: function deactivated()
    /* istanbul ignore next: not easy to test */
    {
      // In case we are inside a `<keep-alive>`
      this.visible = false;
      this.whileOpenListen(false);
      this.removePopper();
    },
    beforeDestroy: function beforeDestroy()
    /* istanbul ignore next: not easy to test */
    {
      this.visible = false;
      this.whileOpenListen(false);
      this.removePopper();
    },
    methods: {
      // Event emitter
      emitEvent: function emitEvent(bvEvt) {
        var type = bvEvt.type;
        this.$emit(type, bvEvt);
        this.$root.$emit("bv::dropdown::".concat(type), bvEvt);
      },
      showMenu: function showMenu() {
        var _this = this;

        if (this.disabled) {
          return;
        } // Ensure other menus are closed


        this.$root.$emit('bv::dropdown::shown', this); // Are we in a navbar ?

        if (this.inNavbar === null && this.isNav) {
          this.inNavbar = Boolean(closest('.navbar', this.$el));
        } // Disable totally Popper.js for Dropdown in Navbar

        /* istanbul ignore next: cant test popper in JSDOM */


        if (!this.inNavbar) {
          if (typeof Popper === 'undefined') {
            warn('b-dropdown: Popper.js not found. Falling back to CSS positioning.');
          } else {
            // for dropup with alignment we use the parent element as popper container
            var element = this.dropup && this.right || this.split ? this.$el : this.$refs.toggle; // Make sure we have a reference to an element, not a component!

            element = element.$el || element; // Instantiate popper.js

            this.createPopper(element);
          }
        }

        this.whileOpenListen(true); // Wrap in nextTick to ensure menu is fully rendered/shown

        this.$nextTick(function () {
          // Focus on the menu container on show
          _this.focusMenu(); // Emit the shown event


          _this.$emit('shown');
        });
      },
      hideMenu: function hideMenu() {
        this.whileOpenListen(false);
        this.$root.$emit('bv::dropdown::hidden', this);
        this.$emit('hidden');
        this.removePopper();
      },
      createPopper: function createPopper(element)
      /* istanbul ignore next: cant test popper in JSDOM */
      {
        this.removePopper();
        this._popper = new Popper(element, this.$refs.menu, this.getPopperConfig());
      },
      removePopper: function removePopper()
      /* istanbul ignore next: cant test popper in JSDOM */
      {
        if (this._popper) {
          // Ensure popper event listeners are removed cleanly
          this._popper.destroy();
        }

        this._popper = null;
      },
      getPopperConfig: function getPopperConfig()
      /* istanbul ignore next: can't test popper in JSDOM */
      {
        var placement = AttachmentMap.BOTTOM;

        if (this.dropup) {
          placement = this.right ? AttachmentMap.TOPEND : AttachmentMap.TOP;
        } else if (this.dropright) {
          placement = AttachmentMap.RIGHT;
        } else if (this.dropleft) {
          placement = AttachmentMap.LEFT;
        } else if (this.right) {
          placement = AttachmentMap.BOTTOMEND;
        }

        var popperConfig = {
          placement: placement,
          modifiers: {
            offset: {
              offset: this.offset || 0
            },
            flip: {
              enabled: !this.noFlip
            }
          }
        };

        if (this.boundary) {
          popperConfig.modifiers.preventOverflow = {
            boundariesElement: this.boundary
          };
        }

        return _objectSpread({}, popperConfig, this.popperOpts || {});
      },
      whileOpenListen: function whileOpenListen(open) {
        // turn listeners on/off while open
        if (open) {
          // If another dropdown is opened
          this.$root.$on('bv::dropdown::shown', this.rootCloseListener); // Hide the dropdown when clicked outside

          this.listenForClickOut = true; // Hide the dropdown when it loses focus

          this.listenForFocusIn = true;
        } else {
          this.$root.$off('bv::dropdown::shown', this.rootCloseListener);
          this.listenForClickOut = false;
          this.listenForFocusIn = false;
        }
      },
      rootCloseListener: function rootCloseListener(vm) {
        if (vm !== this) {
          this.visible = false;
        }
      },
      show: function show() {
        // Public method to show dropdown
        if (this.disabled) {
          return;
        }

        this.visible = true;
      },
      hide: function hide() {
        var refocus = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : false;

        // Public method to hide dropdown
        if (this.disabled) {
          return;
        }

        this.visible = false;

        if (refocus) {
          // Child element is closing the dropdown on click
          this.$once('hidden', this.focusToggler);
        }
      },
      toggle: function toggle(evt) {
        // Called only by a button that toggles the menu
        evt = evt || {};
        var type = evt.type;
        var key = evt.keyCode;

        if (type !== 'click' && !(type === 'keydown' && (key === KeyCodes.ENTER || key === KeyCodes.SPACE || key === KeyCodes.DOWN))) {
          // We only toggle on Click, Enter, Space, and Arrow Down
          return;
        }

        if (this.disabled) {
          this.visible = false;
          return;
        }

        this.$emit('toggle', evt);

        if (evt.defaultPrevented) {
          // Exit if canceled
          return;
        }

        evt.preventDefault();
        evt.stopPropagation(); // Toggle visibility

        this.visible = !this.visible;
      },
      click: function click(evt) {
        // Called only in split button mode, for the split button
        if (this.disabled) {
          this.visible = false;
          return;
        }

        this.$emit('click', evt);
      },
      onKeydown: function onKeydown(evt)
      /* istanbul ignore next: not easy to test */
      {
        // Called from dropdown menu context
        var key = evt.keyCode;

        if (key === KeyCodes.ESC) {
          // Close on ESC
          this.onEsc(evt);
        } else if (key === KeyCodes.TAB) {
          // Close on tab out
          this.onTab(evt);
        } else if (key === KeyCodes.DOWN) {
          // Down Arrow
          this.focusNext(evt, false);
        } else if (key === KeyCodes.UP) {
          // Up Arrow
          this.focusNext(evt, true);
        }
      },
      onEsc: function onEsc(evt)
      /* istanbul ignore next: not easy to test */
      {
        if (this.visible) {
          this.visible = false;
          evt.preventDefault();
          evt.stopPropagation(); // Return focus to original trigger button

          this.$once('hidden', this.focusToggler);
        }
      },
      onTab: function onTab(evt)
      /* istanbul ignore next: not easy to test */
      {// TODO: Need special handler for dealing with form inputs
        // Tab, if in a text-like input, we should just focus next item in the dropdown
        // Note: Inputs are in a special .dropdown-form container
      },
      onMouseOver: function onMouseOver(evt)
      /* istanbul ignore next: not easy to test */
      {// Removed mouseover focus handler
      },
      // Document click out listener
      clickOutHandler: function clickOutHandler() {
        if (this.visible) {
          this.visible = false;
        }
      },
      // Document focusin listener
      focusInHandler: function focusInHandler(evt) {
        // If focus leaves dropdown, hide it
        if (this.visible && !contains(this.$refs.menu, evt.target) && !contains(this.$refs.toggle, evt.target)) {
          this.visible = false;
        }
      },
      // Keyboard nav
      focusNext: function focusNext(evt, up) {
        var _this2 = this;

        if (!this.visible) {
          return;
        }

        evt.preventDefault();
        evt.stopPropagation();
        this.$nextTick(function () {
          var items = _this2.getItems();

          if (items.length < 1) {
            return;
          }

          var index = items.indexOf(evt.target);

          if (up && index > 0) {
            index--;
          } else if (!up && index < items.length - 1) {
            index++;
          }

          if (index < 0) {
            index = 0;
          }

          _this2.focusItem(index, items);
        });
      },
      focusItem: function focusItem(idx, items) {
        var el = items.find(function (el, i) {
          return i === idx;
        });

        if (el && getAttr(el, 'tabindex') !== '-1') {
          el.focus();
        }
      },
      getItems: function getItems() {
        // Get all items
        return filterVisible(selectAll(Selector.ITEM_SELECTOR, this.$refs.menu));
      },
      focusMenu: function focusMenu() {
        this.$refs.menu.focus && this.$refs.menu.focus();
      },
      focusToggler: function focusToggler() {
        var toggler = this.toggler;

        if (toggler && toggler.focus) {
          toggler.focus();
        }
      }
    }
  };

  var BDropdown = {
    name: 'BDropdown',
    components: {
      BButton: BButton
    },
    mixins: [idMixin, dropdownMixin],
    props: {
      toggleText: {
        type: String,
        default: 'Toggle Dropdown'
      },
      size: {
        type: String,
        default: null
      },
      variant: {
        type: String,
        default: null
      },
      menuClass: {
        type: [String, Array],
        default: null
      },
      toggleTag: {
        type: String,
        default: 'button'
      },
      toggleClass: {
        type: [String, Array],
        default: null
      },
      noCaret: {
        type: Boolean,
        default: false
      },
      split: {
        type: Boolean,
        default: false
      },
      splitHref: {
        type: String // default: undefined

      },
      splitTo: {
        type: [String, Object] // default: undefined

      },
      splitVariant: {
        type: String,
        default: null
      },
      role: {
        type: String,
        default: 'menu'
      },
      boundary: {
        // String: `scrollParent`, `window` or `viewport`
        // Object: HTML Element reference
        type: [String, Object],
        default: 'scrollParent'
      }
    },
    computed: {
      dropdownClasses: function dropdownClasses() {
        // Position `static` is needed to allow menu to "breakout" of the scrollParent boundaries
        // when boundary is anything other than `scrollParent`
        // See https://github.com/twbs/bootstrap/issues/24251#issuecomment-341413786
        var positionStatic = this.boundary !== 'scrollParent' || !this.boundary;
        var direction = '';

        if (this.dropup) {
          direction = 'dropup';
        } else if (this.dropright) {
          direction = 'dropright';
        } else if (this.dropleft) {
          direction = 'dropleft';
        }

        return ['btn-group', 'b-dropdown', 'dropdown', direction, {
          show: this.visible,
          'position-static': positionStatic
        }];
      },
      menuClasses: function menuClasses() {
        return ['dropdown-menu', {
          'dropdown-menu-right': this.right,
          show: this.visible
        }, this.menuClass];
      },
      toggleClasses: function toggleClasses() {
        return ['dropdown-toggle', {
          'dropdown-toggle-split': this.split,
          'dropdown-toggle-no-caret': this.noCaret && !this.split
        }, this.toggleClass];
      }
    },
    render: function render(h) {
      var split = h(false);

      if (this.split) {
        var btnProps = {
          disabled: this.disabled,
          variant: this.splitVariant || this.variant,
          size: this.size // We add these as needed due to router-link issues with defined property with undefined/null values

        };

        if (this.splitTo) {
          btnProps.to = this.splitTo;
        }

        if (this.splitHref) {
          btnProps.href = this.splitHref;
        }

        split = h('b-button', {
          ref: 'button',
          props: btnProps,
          attrs: {
            id: this.safeId('_BV_button_')
          },
          on: {
            click: this.click
          }
        }, [this.$slots['button-content'] || this.$slots.text || this.html || stripTags(this.text)]);
      }

      var toggle = h('b-button', {
        ref: 'toggle',
        class: this.toggleClasses,
        props: {
          variant: this.variant,
          size: this.size,
          disabled: this.disabled,
          tag: this.toggleTag
        },
        attrs: {
          id: this.safeId('_BV_toggle_'),
          'aria-haspopup': 'true',
          'aria-expanded': this.visible ? 'true' : 'false'
        },
        on: {
          click: this.toggle,
          // click
          keydown: this.toggle // enter, space, down

        }
      }, [this.split ? h('span', {
        class: ['sr-only']
      }, [this.toggleText]) : this.$slots['button-content'] || this.$slots.text || this.html || stripTags(this.text)]);
      var menu = h('div', {
        ref: 'menu',
        class: this.menuClasses,
        attrs: {
          role: this.role,
          tabindex: '-1',
          'aria-labelledby': this.safeId(this.split ? '_BV_button_' : '_BV_toggle_')
        },
        on: {
          mouseover: this.onMouseOver,
          keydown: this.onKeydown // tab, up, down, esc

        }
      }, [this.$slots.default]);
      return h('div', {
        attrs: {
          id: this.safeId()
        },
        class: this.dropdownClasses
      }, [split, toggle, menu]);
    }
  };

  var props$m = propsFactory(); // @vue/component

  var BDropdownItem = {
    name: 'BDropdownItem',
    inject: {
      dropdown: {
        from: 'dropdown',
        default: null
      }
    },
    props: props$m,
    methods: {
      closeDropdown: function closeDropdown() {
        if (this.dropdown) {
          this.dropdown.hide(true);
        }
      },
      onClick: function onClick(evt) {
        this.$emit('click', evt);
        this.closeDropdown();
      }
    },
    render: function render(h) {
      return h(BLink, {
        props: this.$props,
        staticClass: 'dropdown-item',
        attrs: {
          role: 'menuitem'
        },
        on: {
          click: this.onClick
        }
      }, this.$slots.default);
    }
  };

  var props$n = {
    active: {
      type: Boolean,
      default: false
    },
    activeClass: {
      type: String,
      default: 'active'
    },
    disabled: {
      type: Boolean,
      default: false
    } // @vue/component

  };
  var BDropdownItemButton = {
    name: 'BDropdownItemButton',
    inject: {
      dropdown: {
        from: 'dropdown',
        default: null
      }
    },
    props: props$n,
    methods: {
      closeDropdown: function closeDropdown() {
        if (this.dropdown) {
          this.dropdown.hide(true);
        }
      },
      onClick: function onClick(evt) {
        this.$emit('click', evt);
        this.closeDropdown();
      }
    },
    render: function render(h) {
      return h('button', {
        staticClass: 'dropdown-item',
        class: _defineProperty({}, this.activeClass, this.active),
        attrs: {
          role: 'menuitem',
          type: 'button',
          disabled: this.disabled
        },
        on: {
          click: this.onClick
        }
      }, this.$slots.default);
    }
  };

  var props$o = {
    id: {
      type: String,
      default: null
    },
    tag: {
      type: String,
      default: 'h6'
    } // @vue/component

  };
  var BDropdownHeader = {
    name: 'BDropdownHeader',
    functional: true,
    props: props$o,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        staticClass: 'dropdown-header',
        attrs: {
          id: props.id || null
        }
      }), children);
    }
  };

  var props$p = {
    tag: {
      type: String,
      default: 'div'
    } // @vue/component

  };
  var BDropdownDivider = {
    name: 'BDropdownDivider',
    functional: true,
    props: props$p,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data;
      return h(props.tag, mergeData(data, {
        staticClass: 'dropdown-divider',
        attrs: {
          role: 'separator'
        }
      }));
    }
  };

  var props$q = {
    id: {
      type: String,
      default: null
    },
    inline: {
      type: Boolean,
      default: false
    },
    novalidate: {
      type: Boolean,
      default: false
    },
    validated: {
      type: Boolean,
      default: false
    } // @vue/component

  };
  var BForm = {
    name: 'BForm',
    functional: true,
    props: props$q,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h('form', mergeData(data, {
        class: {
          'form-inline': props.inline,
          'was-validated': props.validated
        },
        attrs: {
          id: props.id,
          novalidate: props.novalidate
        }
      }), children);
    }
  };

  var BDropdownForm = {
    name: 'BDropdownForm',
    functional: true,
    props: _objectSpread({}, props$q),
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(BForm, mergeData(data, {
        props: props,
        staticClass: 'b-dropdown-form'
      }), children);
    }
  };

  var BDropdownText = {
    name: 'BDropdownText',
    functional: true,
    props: {
      tag: {
        type: String,
        default: 'p'
      }
    },
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        props: props,
        staticClass: 'b-dropdown-text'
      }), children);
    }
  };

  var components$b = {
    BDropdown: BDropdown,
    BDd: BDropdown,
    BDropdownItem: BDropdownItem,
    BDdItem: BDropdownItem,
    BDropdownItemButton: BDropdownItemButton,
    BDropdownItemBtn: BDropdownItemButton,
    BDdItemButton: BDropdownItemButton,
    BDdItemBtn: BDropdownItemButton,
    BDropdownHeader: BDropdownHeader,
    BDdHeader: BDropdownHeader,
    BDropdownDivider: BDropdownDivider,
    BDdDivider: BDropdownDivider,
    BDropdownForm: BDropdownForm,
    BDdForm: BDropdownForm,
    BDropdownText: BDropdownText,
    BDdText: BDropdownText
  };
  var dropdownPlugin = {
    install: function install(Vue) {
      registerComponents(Vue, components$b);
    }
  };

  var props$r = {
    type: {
      type: String,
      default: 'iframe',
      validator: function validator(str) {
        return arrayIncludes(['iframe', 'embed', 'video', 'object', 'img', 'b-img', 'b-img-lazy'], str);
      }
    },
    tag: {
      type: String,
      default: 'div'
    },
    aspect: {
      type: String,
      default: '16by9'
    } // @vue/component

  };
  var BEmbed = {
    name: 'BEmbed',
    functional: true,
    props: props$r,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, {
        ref: data.ref,
        staticClass: 'embed-responsive',
        class: _defineProperty({}, "embed-responsive-".concat(props.aspect), Boolean(props.aspect))
      }, [h(props.type, mergeData(data, {
        ref: '',
        staticClass: 'embed-responsive-item'
      }), children)]);
    }
  };

  var components$c = {
    BEmbed: BEmbed
  };
  var index$a = {
    install: function install(Vue) {
      registerComponents(Vue, components$c);
    }
  };

  var props$s = {
    id: {
      type: String,
      default: null
    },
    tag: {
      type: String,
      default: 'small'
    },
    textVariant: {
      type: String,
      default: 'muted'
    },
    inline: {
      type: Boolean,
      default: false
    } // @vue/component

  };
  var BFormText = {
    name: 'BFormText',
    functional: true,
    props: props$s,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        class: _defineProperty({
          'form-text': !props.inline
        }, "text-".concat(props.textVariant), Boolean(props.textVariant)),
        attrs: {
          id: props.id
        }
      }), children);
    }
  };

  var props$t = {
    id: {
      type: String,
      default: null
    },
    tag: {
      type: String,
      default: 'div'
    },
    tooltip: {
      type: Boolean,
      default: false
    },
    forceShow: {
      type: Boolean,
      default: false
    },
    state: {
      type: [Boolean, String],
      default: null
    } // @vue/component

  };
  var BFormInvalidFeedback = {
    name: 'BFormInvalidFeedback',
    functional: true,
    props: props$t,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var show = props.forceShow === true || props.state === false || props.state === 'invalid';
      return h(props.tag, mergeData(data, {
        class: {
          'invalid-feedback': !props.tooltip,
          'invalid-tooltip': props.tooltip,
          'd-block': show
        },
        attrs: {
          id: props.id
        }
      }), children);
    }
  };

  var props$u = {
    id: {
      type: String,
      default: null
    },
    tag: {
      type: String,
      default: 'div'
    },
    tooltip: {
      type: Boolean,
      default: false
    },
    forceShow: {
      type: Boolean,
      default: false
    },
    state: {
      type: [Boolean, String],
      default: null
    } // @vue/component

  };
  var BFormValidFeedback = {
    name: 'BFormValidFeedback',
    functional: true,
    props: props$u,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var show = props.forceShow === true || props.state === true || props.state === 'valid';
      return h(props.tag, mergeData(data, {
        class: {
          'valid-feedback': !props.tooltip,
          'valid-tooltip': props.tooltip,
          'd-block': show
        },
        attrs: {
          id: props.id
        }
      }), children);
    }
  };

  var components$d = {
    BForm: BForm,
    BFormRow: BFormRow,
    BFormText: BFormText,
    BFormInvalidFeedback: BFormInvalidFeedback,
    BFormFeedback: BFormInvalidFeedback,
    BFormValidFeedback: BFormValidFeedback
  };
  var index$b = {
    install: function install(Vue) {
      registerComponents(Vue, components$d);
    }
  };

  /* Form control contextual state class computation
   *
   * Returned class is either 'is-valid' or 'is-invalid' based on the 'state' prop
   * state can be one of five values:
   *  - true or 'valid' for is-valid
   *  - false or 'invalid' for is-invalid
   *  - null (or empty string) for no contextual state
   */
  // @vue/component
  var formStateMixin = {
    props: {
      state: {
        // true/'valid', false/'invalid', '',null
        // The order must be String first, then Boolean!
        type: [String, Boolean],
        default: null
      }
    },
    computed: {
      computedState: function computedState() {
        var state = this.state;

        if (state === '') {
          return null;
        } else if (state === true || state === 'valid') {
          return true;
        } else if (state === false || state === 'invalid') {
          return false;
        }

        return null;
      },
      stateClass: function stateClass() {
        var state = this.computedState;

        if (state === true) {
          return 'is-valid';
        } else if (state === false) {
          return 'is-invalid';
        }

        return null;
      }
    }
  };

  var SELECTOR = 'input:not(:disabled),textarea:not(:disabled),select:not(:disabled)'; // Breakpoint names for label-cols and label-align props

  var BREAKPOINTS$1 = ['', 'sm', 'md', 'lg', 'xl']; // Memoize this function to return cached values to save time in computed functions

  var makePropName = memoize(function () {
    var breakpoint = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
    var prefix = arguments.length > 1 ? arguments[1] : undefined;
    return "".concat(prefix).concat(upperFirst(breakpoint));
  }); // Generate the labelCol breakpoint props

  var bpLabelColProps = BREAKPOINTS$1.reduce(function (props, breakpoint) {
    // label-cols, label-cols-sm, label-cols-md, ...
    props[makePropName(breakpoint, 'labelCols')] = {
      type: [Number, String, Boolean],
      default: breakpoint ? false : null
    };
    return props;
  }, create(null)); // Generate the labelAlign breakpoint props

  var bpLabelAlignProps = BREAKPOINTS$1.reduce(function (props, breakpoint) {
    // label-align, label-align-sm, label-align-md, ...
    props[makePropName(breakpoint, 'labelAlign')] = {
      type: String,
      // left, right, center
      default: null
    };
    return props;
  }, create(null)); // render helper functions (here rather than polluting the instance with more methods)

  function renderInvalidFeedback(h, ctx) {
    var content = ctx.$slots['invalid-feedback'] || ctx.invalidFeedback;
    var invalidFeedback = h(false);

    if (content) {
      invalidFeedback = h('b-form-invalid-feedback', {
        props: {
          id: ctx.invalidFeedbackId,
          // If state is explicitly false, always show the feedback
          state: ctx.computedState,
          tooltip: ctx.tooltip
        },
        attrs: {
          tabindex: content ? '-1' : null,
          role: 'alert',
          'aria-live': 'assertive',
          'aria-atomic': 'true'
        }
      }, [content]);
    }

    return invalidFeedback;
  }

  function renderValidFeedback(h, ctx) {
    var content = ctx.$slots['valid-feedback'] || ctx.validFeedback;
    var validFeedback = h(false);

    if (content) {
      validFeedback = h('b-form-valid-feedback', {
        props: {
          id: ctx.validFeedbackId,
          // If state is explicitly true, always show the feedback
          state: ctx.computedState,
          tooltip: ctx.tooltip
        },
        attrs: {
          tabindex: '-1',
          role: 'alert',
          'aria-live': 'assertive',
          'aria-atomic': 'true'
        }
      }, [content]);
    }

    return validFeedback;
  }

  function renderHelpText(h, ctx) {
    // Form help text (description)
    var content = ctx.$slots['description'] || ctx.description;
    var description = h(false);

    if (content) {
      description = h('b-form-text', {
        attrs: {
          id: ctx.descriptionId,
          tabindex: '-1'
        }
      }, [content]);
    }

    return description;
  }

  function renderLabel(h, ctx) {
    // render label/legend inside b-col if necessary
    var content = ctx.$slots['label'] || ctx.label;
    var labelFor = ctx.labelFor;
    var isLegend = !labelFor;
    var isHorizontal = ctx.isHorizontal;
    var labelTag = isLegend ? 'legend' : 'label';

    if (!content && !isHorizontal) {
      return h(false);
    } else if (ctx.labelSrOnly) {
      var label = h(false);

      if (content) {
        label = h(labelTag, {
          class: 'sr-only',
          attrs: {
            id: ctx.labelId,
            for: labelFor || null
          }
        }, [content]);
      }

      return h(isHorizontal ? 'b-col' : 'div', {
        props: isHorizontal ? ctx.labelColProps : {}
      }, [label]);
    } else {
      return h(isHorizontal ? 'b-col' : labelTag, {
        on: isLegend ? {
          click: ctx.legendClick
        } : {},
        props: isHorizontal ? _objectSpread({
          tag: labelTag
        }, ctx.labelColProps) : {},
        attrs: {
          id: ctx.labelId,
          for: labelFor || null,
          // We add a tab index to legend so that screen readers will properly read the aria-labelledby in IE.
          tabindex: isLegend ? '-1' : null
        },
        class: [// When horizontal or if a legend is rendered, add col-form-label for correct sizing
        // as Bootstrap has inconsitent font styling for legend in non-horiontal form-groups.
        // See: https://github.com/twbs/bootstrap/issues/27805
        isHorizontal || isLegend ? 'col-form-label' : '', // Emulate label padding top of 0 on legend when not horizontal
        !isHorizontal && isLegend ? 'pt-0' : '', // If not horizontal and not a legend, we add d-block to label so that label-align works
        !isHorizontal && !isLegend ? 'd-block' : '', ctx.labelSize ? "col-form-label-".concat(ctx.labelSize) : '', ctx.labelAlignClasses, ctx.labelClass]
      }, [content]);
    }
  } // bFormGroup
  // @vue/component


  var BFormGroup = {
    name: 'BFormGroup',
    components: {
      BFormRow: BFormRow,
      BCol: BCol,
      BFormInvalidFeedback: BFormInvalidFeedback,
      BFormValidFeedback: BFormValidFeedback,
      BFormText: BFormText
    },
    mixins: [idMixin, formStateMixin],
    props: _objectSpread({
      label: {
        type: String,
        default: null
      },
      labelFor: {
        type: String,
        default: null
      },
      labelSize: {
        type: String,
        default: null
      },
      labelSrOnly: {
        type: Boolean,
        default: false
      },
      labelClass: {
        type: [String, Array, Object],
        default: null
      },
      description: {
        type: String,
        default: null
      },
      invalidFeedback: {
        type: String,
        default: null
      },
      validFeedback: {
        type: String,
        default: null
      },
      tooltip: {
        // Enable tooltip style feedback
        type: Boolean,
        default: false
      },
      validated: {
        type: Boolean,
        default: false
      },
      disabled: {
        type: Boolean,
        default: false
      }
    }, bpLabelColProps, bpLabelAlignProps, {
      horizontal: {
        // Deprecated
        type: Boolean,
        default: false
      },
      breakpoint: {
        // Deprecated (ignored if horizontal is not true)
        type: String,
        default: null // legacy value 'sm'

      }
    }),
    computed: {
      labelColProps: function labelColProps() {
        var _this = this;

        var props = {};

        if (this.horizontal) {
          // Deprecated setting of horizontal/breakpoint props
          warn("b-form-group: Props 'horizontal' and 'breakpoint' are deprecated. Use 'label-cols(-{breakpoint})' props instead."); // Legacy default is breakpoint sm and cols 3

          var bp = this.breakpoint || 'sm';
          var cols = parseInt(this.labelCols, 10) || 3;
          props[bp] = cols > 0 ? cols : 3; // We then return the single breakpoint prop for legacy compatability

          return props;
        }

        BREAKPOINTS$1.forEach(function (breakpoint) {
          // Grab the value if the label column breakpoint prop
          var propVal = _this[makePropName(breakpoint, 'labelCols')]; // Handle case where the prop's value is an empty string, which represents true


          propVal = propVal === '' ? true : propVal || false;

          if (typeof propVal !== 'boolean') {
            // Convert to column size to number
            propVal = parseInt(propVal, 10) || 0; // Ensure column size is greater than 0

            propVal = propVal > 0 ? propVal : false;
          }

          if (propVal) {
            // Add the prop to the list of props to give to b-col.
            // if breakpoint is '' (labelCols=true), then we use the col prop to make equal width at xs
            var bColPropName = breakpoint || (typeof propVal === 'boolean' ? 'col' : 'cols'); // Add it to the props

            props[bColPropName] = propVal;
          }
        });
        return props;
      },
      labelAlignClasses: function labelAlignClasses() {
        var _this2 = this;

        var classes = [];
        BREAKPOINTS$1.forEach(function (breakpoint) {
          // assemble the label column breakpoint align classes
          var propVal = _this2[makePropName(breakpoint, 'labelAlign')] || null;

          if (propVal) {
            var className = breakpoint ? "text-".concat(breakpoint, "-").concat(propVal) : "text-".concat(propVal);
            classes.push(className);
          }
        });
        return classes;
      },
      isHorizontal: function isHorizontal() {
        // Determine if the resultant form-group will be rendered
        // horizontal (meaning it has label-col breakpoints)
        return keys(this.labelColProps).length > 0;
      },
      labelId: function labelId() {
        return this.$slots['label'] || this.label ? this.safeId('_BV_label_') : null;
      },
      descriptionId: function descriptionId() {
        return this.$slots['description'] || this.description ? this.safeId('_BV_description_') : null;
      },
      hasInvalidFeedback: function hasInvalidFeedback() {
        // used for computing aria-describedby
        var $slots = this.$slots;
        return this.computedState === false && ($slots['invalid-feedback'] || this.invalidFeedback);
      },
      invalidFeedbackId: function invalidFeedbackId() {
        return this.hasInvalidFeedback ? this.safeId('_BV_feedback_invalid_') : null;
      },
      hasValidFeedback: function hasValidFeedback() {
        // used for computing aria-describedby
        return this.computedState === true && (this.$slots['valid-feedback'] || this.validFeedback);
      },
      validFeedbackId: function validFeedbackId() {
        return this.hasValidFeedback ? this.safeId('_BV_feedback_valid_') : null;
      },
      describedByIds: function describedByIds() {
        // Screen readers will read out any content linked to by aria-describedby
        // even if the content is hidden with 'display: none', hence we only include
        // feedback IDs if the form-group's state is explicitly valid or invalid.
        return [this.descriptionId, this.invalidFeedbackId, this.validFeedbackId].filter(function (i) {
          return i;
        }).join(' ') || null;
      }
    },
    watch: {
      describedByIds: function describedByIds(add, remove) {
        if (add !== remove) {
          this.setInputDescribedBy(add, remove);
        }
      }
    },
    mounted: function mounted() {
      var _this3 = this;

      this.$nextTick(function () {
        // Set the adia-describedby IDs on the input specified by label-for
        // We do this in a nextTick to ensure the children have finished rendering
        _this3.setInputDescribedBy(_this3.describedByIds);
      });
    },
    methods: {
      legendClick: function legendClick(evt) {
        if (this.labelFor) {
          // don't do anything if labelFor is set
          return;
        }

        var tagName = evt.target ? evt.target.tagName : '';

        if (/^(input|select|textarea|label|button|a)$/i.test(tagName)) {
          // If clicked an interactive element inside legend, we just let the default happen
          return;
        }

        var inputs = selectAll(SELECTOR, this.$refs.content).filter(isVisible);

        if (inputs && inputs.length === 1 && inputs[0].focus) {
          // if only a single input, focus it, emulating label behaviour
          inputs[0].focus();
        }
      },
      setInputDescribedBy: function setInputDescribedBy(add, remove) {
        // Sets the `aria-describedby` attribute on the input if label-for is set.
        // Optionally accepts a string of IDs to remove as the second parameter
        if (this.labelFor && typeof document !== 'undefined') {
          var input = select("#".concat(this.labelFor), this.$refs.content);

          if (input) {
            var adb = 'aria-describedby';
            var ids = (getAttr(input, adb) || '').split(/\s+/);
            remove = (remove || '').split(/\s+/); // Update ID list, preserving any original IDs

            ids = ids.filter(function (id) {
              return !arrayIncludes(remove, id);
            }).concat(add || '').join(' ').trim();

            if (ids) {
              setAttr(input, adb, ids);
            } else {
              // No IDs, so remove the attribute
              removeAttr(input, adb);
            }
          }
        }
      }
    },
    render: function render(h) {
      var isFieldset = !this.labelFor;
      var isHorizontal = this.isHorizontal; // Generate the label

      var label = renderLabel(h, this); // Generate the content

      var content = h(isHorizontal ? 'b-col' : 'div', {
        ref: 'content',
        attrs: {
          tabindex: isFieldset ? '-1' : null,
          role: isFieldset ? 'group' : null,
          'aria-labelledby': isFieldset ? this.labelId : null,
          'aria-describedby': isFieldset ? this.ariaDescribedBy : null
        }
      }, [this.$slots['default'] || h(false), renderInvalidFeedback(h, this), renderValidFeedback(h, this), renderHelpText(h, this)]); // Create the form-group

      var data = {
        staticClass: 'form-group',
        class: [this.validated ? 'was-validated' : null, this.stateClass],
        attrs: {
          id: this.safeId(),
          disabled: isFieldset ? this.disabled : null,
          role: isFieldset ? null : 'group',
          'aria-invalid': this.computedState === false ? 'true' : null,
          'aria-labelledby': this.labelId || null,
          'aria-describedby': this.describedByIds || null
        } // Return it wrapped in a form-group.
        // Note: fieldsets do not support adding `row` or `form-row` directly to them
        // due to browser specific render issues, so we move the form-row to an
        // inner wrapper div when horizontal and using a fieldset

      };
      return h(isFieldset ? 'fieldset' : isHorizontal ? 'b-form-row' : 'div', data, isHorizontal && isFieldset ? [h('b-form-row', {}, [label, content])] : [label, content]);
    }
  };

  var components$e = {
    BFormGroup: BFormGroup,
    BFormFieldset: BFormGroup
  };
  var index$c = {
    install: function install(Vue) {
      registerComponents(Vue, components$e);
    }
  };

  // @vue/component
  var formRadioCheckMixin = {
    model: {
      prop: 'checked',
      event: 'input'
    },
    props: {
      value: {// value when checked
        // type: Object,
        // default: undefined
      },
      checked: {// This is the v-model
        // type: Object,
        // default: undefined
      },
      inline: {
        type: Boolean,
        default: false
      },
      plain: {
        type: Boolean,
        default: false
      },
      button: {
        // only aplicable in standalone mode (non group)
        type: Boolean,
        default: false
      },
      buttonVariant: {
        // Only applicable when rendered with button style
        type: String,
        default: null
      }
    },
    data: function data() {
      return {
        localChecked: this.bvGroup.checked,
        hasFocus: false,
        // Surrogate value when not a childe of group
        buttons: false
      };
    },
    computed: {
      computedLocalChecked: {
        get: function get() {
          return this.bvGroup.localChecked;
        },
        set: function set(val) {
          this.bvGroup.localChecked = val;
        }
      },
      is_Group: function is_Group() {
        // Is this check/radio a child of check-group or radio-group?
        return this.bvGroup !== this;
      },
      is_BtnMode: function is_BtnMode() {
        // Support button style in single input mode
        return this.is_Group ? this.bvGroup.buttons : this.button;
      },
      is_Plain: function is_Plain() {
        return this.is_BtnMode ? false : this.bvGroup.plain;
      },
      is_Custom: function is_Custom() {
        return this.is_BtnMode ? false : !this.bvGroup.plain;
      },
      is_Switch: function is_Switch() {
        // Custom switch styling (checkboxes only)
        return this.is_BtnMode || this.is_Radio || this.is_Plain ? false : this.is_Group ? this.bvGroup.switches : this.switch;
      },
      is_Inline: function is_Inline() {
        return this.bvGroup.inline;
      },
      is_Disabled: function is_Disabled() {
        // Child can be disabled while parent isn't, but is always disabled if group is
        return this.bvGroup.disabled || this.disabled;
      },
      is_Required: function is_Required() {
        // Required only works when a name is provided for the input(s)
        return Boolean(this.get_Name && this.bvGroup.required);
      },
      get_Name: function get_Name() {
        // Group name preferred over local name
        return this.bvGroup.groupName || this.name || null;
      },
      get_Form: function get_Form() {
        return this.bvGroup.form || null;
      },
      get_Size: function get_Size() {
        return this.bvGroup.size || '';
      },
      get_State: function get_State() {
        // local state preferred over group state (except when null)
        if (typeof this.computedState === 'boolean') {
          return this.computedState;
        } else if (typeof this.bvGroup.computedState === 'boolean') {
          return this.bvGroup.computedState;
        } else {
          return null;
        }
      },
      get_ButtonVariant: function get_ButtonVariant() {
        // Local variant preferred over group variant
        return this.buttonVariant || this.bvGroup.buttonVariant || 'secondary';
      },
      buttonClasses: function buttonClasses() {
        // Same for radio & check
        return ['btn', "btn-".concat(this.get_ButtonVariant), this.get_Size ? "btn-".concat(this.get_Size) : '', // 'disabled' class makes "button" look disabled
        this.is_Disabled ? 'disabled' : '', // 'active' class makes "button" look pressed
        this.is_Checked ? 'active' : '', // Focus class makes button look focused
        this.hasFocus ? 'focus' : ''];
      }
    },
    watch: {
      checked: function checked(newVal, oldVal) {
        this.computedLocalChecked = newVal;
      }
    },
    methods: {
      handleFocus: function handleFocus(evt) {
        // When in buttons mode, we need to add 'focus' class to label when input focused
        if (evt.target) {
          if (evt.type === 'focus') {
            this.hasFocus = true;
          } else if (evt.type === 'blur') {
            this.hasFocus = false;
          }
        }
      }
    },
    render: function render(h) {
      var defaultSlot = this.$slots.default; // Generate the input element

      var on = {
        change: this.handleChange
      };

      if (this.is_BtnMode) {
        // handlers for focus styling when in button mode
        on.focus = on.blur = this.handleFocus;
      }

      var input = h('input', {
        ref: 'input',
        key: 'input',
        on: on,
        class: {
          'form-check-input': this.is_Plain,
          'custom-control-input': this.is_Custom,
          'is-valid': this.get_State === true && !this.is_BtnMode,
          'is-invalid': this.get_State === false && !this.is_BtnMode
        },
        directives: [{
          name: 'model',
          rawName: 'v-model',
          value: this.computedLocalChecked,
          expression: 'computedLocalChecked'
        }],
        attrs: {
          id: this.safeId(),
          type: this.is_Radio ? 'radio' : 'checkbox',
          name: this.get_Name,
          form: this.get_Form,
          disabled: this.is_Disabled,
          required: this.is_Required,
          autocomplete: 'off',
          'aria-required': this.is_Required || null
        },
        domProps: {
          value: this.value,
          checked: this.is_Checked
        }
      });

      if (this.is_BtnMode) {
        // Button mode
        var button = h('label', {
          class: this.buttonClasses
        }, [input, defaultSlot]);

        if (!this.is_Group) {
          // Standalone button mode, so wrap in 'btn-group-toggle'
          // and flag it as inline-block to mimic regular buttons
          button = h('div', {
            class: ['btn-group-toggle', 'd-inline-block']
          }, [button]);
        }

        return button;
      } else {
        // Not button mode
        var label = h('label', {
          class: {
            'form-check-label': this.is_Plain,
            'custom-control-label': this.is_Custom
          },
          attrs: {
            for: this.safeId()
          }
        }, defaultSlot); // Wrap it in a div

        return h('div', {
          class: _defineProperty({
            'form-check': this.is_Plain,
            'form-check-inline': this.is_Plain && this.is_Inline,
            'custom-control': this.is_Custom,
            'custom-control-inline': this.is_Custom && this.is_Inline,
            'custom-checkbox': this.is_Custom && this.is_Check && !this.is_Switch,
            'custom-switch': this.is_Switch,
            'custom-radio': this.is_Custom && this.is_Radio
          }, "form-control-".concat(this.get_Size), Boolean(this.get_Size && !this.is_BtnMode))
        }, [input, label]);
      }
    }
  };

  // @vue/component
  var formMixin = {
    props: {
      name: {
        type: String // default: undefined

      },
      id: {
        type: String // default: undefined

      },
      disabled: {
        type: Boolean
      },
      required: {
        type: Boolean,
        default: false
      },
      form: {
        type: String,
        default: null
      }
    }
  };

  // @vue/component
  var formSizeMixin = {
    props: {
      size: {
        type: String,
        default: null
      }
    },
    computed: {
      sizeFormClass: function sizeFormClass() {
        return [this.size ? "form-control-".concat(this.size) : null];
      },
      sizeBtnClass: function sizeBtnClass() {
        return [this.size ? "btn-".concat(this.size) : null];
      }
    }
  };

  function isDate(obj) {
    return obj instanceof Date;
  }

  function isFile(obj) {
    return obj instanceof File;
  }
  /**
   * Quick object check - this is primarily used to tell
   * Objects from primitive values when we know the value
   * is a JSON-compliant type.
   * Note object could be a complex type like array, date, etc.
   */


  function isObject(obj) {
    return obj !== null && _typeof(obj) === 'object';
  }
  /**
   * Check if two values are loosely equal - that is,
   * if they are plain objects, do they have the same shape?
   * Returns boolean true or false
   */


  function looseEqual(a, b) {
    if (a === b) {
      return true;
    }

    if (_typeof(a) !== _typeof(b)) {
      return false;
    }

    var validTypesCount = [isDate(a), isDate(b)].filter(Boolean).length;

    if (validTypesCount > 0) {
      return validTypesCount === 2 ? a.getTime() === b.getTime() : false;
    }

    validTypesCount = [isFile(a), isFile(b)].filter(Boolean).length;

    if (validTypesCount > 0) {
      return validTypesCount === 2 ? a === b : false;
    }

    validTypesCount = [isArray(a), isArray(b)].filter(Boolean).length;

    if (validTypesCount > 0) {
      return validTypesCount === 2 ? a.length === b.length && a.every(function (e, i) {
        return looseEqual(e, b[i]);
      }) : false;
    }

    validTypesCount = [isObject(a), isObject(b)].filter(Boolean).length;

    if (validTypesCount > 0) {
      /* istanbul ignore if: this if will probably never be called */
      if (validTypesCount === 1) {
        return false;
      }

      var aKeysCount = keys(a).length;
      var bKeysCount = keys(b).length;

      if (aKeysCount !== bKeysCount) {
        return false;
      }

      if (aKeysCount === 0 && bKeysCount === 0) {
        return String(a) === String(b);
      } // Using for loop over `Object.keys()` here since some class
      // keys are not handled correctly otherwise


      for (var key in a) {
        if ([a.hasOwnProperty(key), b.hasOwnProperty(key)].filter(Boolean).length === 1 || !looseEqual(a[key], b[key])) {
          return false;
        }
      }

      return true;
    }

    return false;
  }

  function looseIndexOf (arr, val) {
    // Assumes that the first argument is an array
    for (var i = 0; i < arr.length; i++) {
      if (looseEqual(arr[i], val)) {
        return i;
      }
    }

    return -1;
  }

  var BFormCheckbox = {
    name: 'BFormCheckbox',
    mixins: [formRadioCheckMixin, // includes shared render function
    idMixin, formMixin, formSizeMixin, formStateMixin],
    inject: {
      bvGroup: {
        from: 'bvCheckGroup',
        default: function _default() {
          return this;
        }
      }
    },
    props: {
      value: {
        // type: [Object, Boolean],
        default: true
      },
      uncheckedValue: {
        // type: [Object, Boolean],
        // Not applicable in multi-check mode
        default: false
      },
      indeterminate: {
        // Not applicable in multi-check mode
        type: Boolean,
        default: false
      },
      switch: {
        // Custom switch styling
        type: Boolean,
        default: false
      },
      checked: {
        // v-model
        type: [String, Number, Object, Array, Boolean],
        default: null
      }
    },
    computed: {
      is_Checked: function is_Checked() {
        var checked = this.computedLocalChecked;
        var value = this.value;

        if (isArray(checked)) {
          return looseIndexOf(checked, value) > -1;
        } else {
          return looseEqual(checked, value);
        }
      },
      is_Radio: function is_Radio() {
        return false;
      },
      is_Check: function is_Check() {
        return true;
      }
    },
    watch: {
      computedLocalChecked: function computedLocalChecked(newVal, oldVal) {
        this.$emit('input', newVal);

        if (this.$refs && this.$refs.input) {
          this.$emit('update:indeterminate', this.$refs.input.indeterminate);
        }
      },
      indeterminate: function indeterminate(newVal, oldVal) {
        this.setIndeterminate(newVal);
      }
    },
    mounted: function mounted() {
      // Set initial indeterminate state
      this.setIndeterminate(this.indeterminate);
    },
    methods: {
      handleChange: function handleChange(_ref) {
        var _ref$target = _ref.target,
            checked = _ref$target.checked,
            indeterminate = _ref$target.indeterminate;
        var localChecked = this.computedLocalChecked;
        var value = this.value;
        var isArr = isArray(localChecked);
        var uncheckedValue = isArr ? null : this.uncheckedValue; // Update computedLocalChecked

        if (isArr) {
          var idx = looseIndexOf(localChecked, value);

          if (checked && idx < 0) {
            // add value to array
            localChecked = localChecked.concat(value);
          } else if (!checked && idx > -1) {
            // remove value from array
            localChecked = localChecked.slice(0, idx).concat(localChecked.slice(idx + 1));
          }
        } else {
          localChecked = checked ? value : uncheckedValue;
        }

        this.computedLocalChecked = localChecked; // Change is only emitted on user interaction

        this.$emit('change', checked ? value : uncheckedValue); // If this is a child of form-checkbox-group, we emit a change event on it as well

        if (this.is_Group) {
          this.bvGroup.$emit('change', localChecked);
        }

        this.$emit('update:indeterminate', indeterminate);
      },
      setIndeterminate: function setIndeterminate(state) {
        // Indeterminate only supported in single checkbox mode
        if (isArray(this.computedLocalChecked)) {
          state = false;
        }

        if (this.$refs && this.$refs.input) {
          this.$refs.input.indeterminate = state; // Emit update event to prop

          this.$emit('update:indeterminate', state);
        }
      }
    }
  };

  function isObject$1(obj) {
    return obj && {}.toString.call(obj) === '[object Object]';
  } // @vue/component


  var formOptionsMixin = {
    props: {
      options: {
        type: [Array, Object],
        default: function _default() {
          return [];
        }
      },
      valueField: {
        type: String,
        default: 'value'
      },
      textField: {
        type: String,
        default: 'text'
      },
      htmlField: {
        type: String,
        default: 'html'
      },
      disabledField: {
        type: String,
        default: 'disabled'
      }
    },
    computed: {
      formOptions: function formOptions() {
        var options = this.options;
        var valueField = this.valueField;
        var textField = this.textField;
        var htmlField = this.htmlField;
        var disabledField = this.disabledField;

        if (isArray(options)) {
          // Normalize flat-ish arrays to Array of Objects
          return options.map(function (option) {
            if (isObject$1(option)) {
              return {
                value: option[valueField],
                text: stripTags(String(option[textField])),
                html: option[htmlField],
                disabled: option[disabledField] || false
              };
            }

            return {
              value: option,
              text: stripTags(String(option)),
              disabled: false
            };
          });
        } else {
          // options is Object
          // Normalize Objects to Array of Objects
          return keys(options).map(function (key) {
            var option = options[key] || {};

            if (isObject$1(option)) {
              var value = option[valueField];
              var text = option[textField];
              return {
                value: typeof value === 'undefined' ? key : value,
                text: typeof text === 'undefined' ? key : stripTags(String(text)),
                html: option[htmlField],
                disabled: option[disabledField] || false
              };
            }

            return {
              value: key,
              text: stripTags(String(option)),
              disabled: false
            };
          });
        }
      }
    }
  };

  var formRadioCheckGroupMixin = {
    model: {
      prop: 'checked',
      event: 'input'
    },
    props: {
      validated: {
        type: Boolean,
        default: false
      },
      ariaInvalid: {
        type: [Boolean, String],
        default: false
      },
      stacked: {
        type: Boolean,
        default: false
      },
      plain: {
        type: Boolean,
        default: false
      },
      buttons: {
        // Render as button style
        type: Boolean,
        default: false
      },
      buttonVariant: {
        // Only applicable when rendered with button style
        type: String,
        default: 'secondary'
      }
    },
    computed: {
      inline: function inline() {
        return !this.stacked;
      },
      groupName: function groupName() {
        // checks/radios tied to the same model must have the sanme name,
        // especially for ARIA accessibility.
        return this.name || this.safeId();
      },
      groupClasses: function groupClasses() {
        if (this.buttons) {
          return ['btn-group-toggle', this.inline ? 'btn-group' : 'btn-group-vertical', this.size ? "btn-group-".concat(this.size) : '', this.validated ? "was-validated" : ''];
        }

        return [// is this needed since children will pick up on size?
        this.sizeFormClass, this.validated ? "was-validated" : ''];
      },
      computedAriaInvalid: function computedAriaInvalid() {
        var ariaInvalid = this.ariaInvalid;

        if (ariaInvalid === true || ariaInvalid === 'true' || ariaInvalid === '') {
          return 'true';
        }

        return this.computedState === false ? 'true' : null;
      }
    },
    watch: {
      checked: function checked(newVal, oldVal) {
        this.localChecked = newVal;
      },
      localChecked: function localChecked(newVal, oldVal) {
        this.$emit('input', newVal);
      }
    },
    render: function render(h) {
      var _this = this;

      var $slots = this.$slots;
      var inputs = this.formOptions.map(function (option, idx) {
        var uid = "_BV_option_".concat(idx, "_");
        return h(_this.is_RadioGroup ? 'b-form-radio' : 'b-form-checkbox', {
          key: uid,
          props: {
            id: _this.safeId(uid),
            value: option.value,
            disabled: option.disabled || null // Do we need to do these, since radio's will know they are inside here?
            // name: this.groupName,
            // form: this.form || null,
            // required: Boolean(this.name && this.required),

          }
        }, [h('span', {
          domProps: htmlOrText(option.html, option.text)
        })]);
      });
      return h('div', {
        class: this.groupClasses,
        attrs: {
          id: this.safeId(),
          role: this.is_RadioGroup ? 'radiogroup' : 'group',
          // Tabindex to allow group to be focused if needed
          tabindex: '-1',
          'aria-required': this.required ? 'true' : null,
          'aria-invalid': this.computedAriaInvalid
        }
      }, [$slots.first, inputs, $slots.default]);
    }
  };

  var BFormCheckboxGroup = {
    name: 'BFormCheckboxGroup',
    components: {
      BFormCheckbox: BFormCheckbox
    },
    mixins: [idMixin, formMixin, formRadioCheckGroupMixin, // includes render function
    formOptionsMixin, formSizeMixin, formStateMixin],
    provide: function provide() {
      return {
        bvCheckGroup: this
      };
    },
    props: {
      switches: {
        // Custom switch styling
        type: Boolean,
        default: false
      },
      checked: {
        type: [String, Number, Object, Array, Boolean],
        default: null
      }
    },
    data: function data() {
      return {
        localChecked: this.checked || []
      };
    },
    computed: {
      is_RadioGroup: function is_RadioGroup() {
        return false;
      }
    }
  };

  var components$f = {
    BFormCheckbox: BFormCheckbox,
    BCheckbox: BFormCheckbox,
    BCheck: BFormCheckbox,
    BFormCheckboxGroup: BFormCheckboxGroup,
    BCheckboxGroup: BFormCheckboxGroup,
    BCheckGroup: BFormCheckboxGroup
  };
  var index$d = {
    install: function install(Vue) {
      registerComponents(Vue, components$f);
    }
  };

  var BFormRadio = {
    name: 'BFormRadio',
    mixins: [idMixin, formRadioCheckMixin, // includes shared render function
    formMixin, formSizeMixin, formStateMixin],
    inject: {
      bvGroup: {
        from: 'bvRadioGroup',
        default: function _default() {
          return this;
        }
      }
    },
    props: {
      checked: {
        // v-model
        type: [String, Object, Number, Boolean],
        default: null
      }
    },
    computed: {
      // Radio Groups can only have a single value, so determining if checked is simple
      is_Checked: function is_Checked() {
        return looseEqual(this.value, this.computedLocalChecked);
      },
      is_Radio: function is_Radio() {
        return true;
      },
      is_Check: function is_Check() {
        return false;
      }
    },
    watch: {
      // Radio Groups can only have a single value, so our watchers are simple
      computedLocalChecked: function computedLocalChecked(newVal, oldVal) {
        this.$emit('input', this.computedLocalChecked);
      }
    },
    methods: {
      handleChange: function handleChange(_ref) {
        var checked = _ref.target.checked;
        var value = this.value;
        this.computedLocalChecked = value; // Change is only emitted on user interaction

        this.$emit('change', checked ? value : null); // If this is a child of form-radio-group, we emit a change event on it as well

        if (this.is_Group) {
          this.bvGroup.$emit('change', checked ? value : null);
        }
      }
    }
  };

  var BFormRadioGroup = {
    name: 'BFormRadioGroup',
    components: {
      BFormRadio: BFormRadio
    },
    mixins: [idMixin, formMixin, formRadioCheckGroupMixin, // includes render function
    formOptionsMixin, formSizeMixin, formStateMixin],
    provide: function provide() {
      return {
        bvRadioGroup: this
      };
    },
    props: {
      checked: {
        type: [String, Object, Number, Boolean],
        default: null
      }
    },
    data: function data() {
      return {
        localChecked: this.checked
      };
    },
    computed: {
      is_RadioGroup: function is_RadioGroup() {
        return true;
      }
    }
  };

  var components$g = {
    BFormRadio: BFormRadio,
    BRadio: BFormRadio,
    BFormRadioGroup: BFormRadioGroup,
    BRadioGroup: BFormRadioGroup
  };
  var index$e = {
    install: function install(Vue) {
      registerComponents(Vue, components$g);
    }
  };

  // @vue/component
  var formTextMixin = {
    model: {
      prop: 'value',
      event: 'update'
    },
    props: {
      value: {
        type: String,
        default: ''
      },
      ariaInvalid: {
        type: [Boolean, String],
        default: false
      },
      readonly: {
        type: Boolean,
        default: false
      },
      plaintext: {
        type: Boolean,
        default: false
      },
      autocomplete: {
        type: String,
        default: null
      },
      placeholder: {
        type: String,
        default: null
      },
      formatter: {
        type: Function,
        default: null
      },
      trim: {
        type: Boolean,
        default: false
      },
      number: {
        type: Boolean,
        default: false
      },
      lazyFormatter: {
        type: Boolean,
        value: false
      }
    },
    data: function data() {
      return {
        localValue: this.stringifyValue(this.value)
      };
    },
    computed: {
      computedClass: function computedClass() {
        return [{
          // Range input needs class custom-range
          'custom-range': this.type === 'range',
          // plaintext not supported by type=range or type=color
          'form-control-plaintext': this.plaintext && this.type !== 'range' && this.type !== 'color',
          // form-control not used by type=range or plaintext. Always used by type=color
          'form-control': !this.plaintext && this.type !== 'range' || this.type === 'color'
        }, this.sizeFormClass, this.stateClass];
      },
      computedAriaInvalid: function computedAriaInvalid() {
        if (!this.ariaInvalid || this.ariaInvalid === 'false') {
          // this.ariaInvalid is null or false or 'false'
          return this.computedState === false ? 'true' : null;
        }

        if (this.ariaInvalid === true) {
          // User wants explicit aria-invalid=true
          return 'true';
        } // Most likely a string value (which could be the string 'true')


        return this.ariaInvalid;
      }
    },
    watch: {
      value: function value(newVal, oldVal) {
        if (newVal !== oldVal && newVal !== this.localValue) {
          this.localValue = this.stringifyValue(newVal);
        }
      }
    },
    mounted: function mounted() {
      var value = this.stringifyValue(this.value);

      if (value !== this.localValue) {
        this.localValue = value;
      }
    },
    methods: {
      stringifyValue: function stringifyValue(value) {
        return value === null || typeof value === 'undefined' ? '' : String(value);
      },
      getFormatted: function getFormatted(value, event) {
        var force = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
        value = this.stringifyValue(value);

        if ((!this.lazyFormatter || force) && typeof this.formatter === 'function') {
          value = this.formatter(value, event);
        }

        return value;
      },
      updateValue: function updateValue(value) {
        value = this.stringifyValue(value);

        if (this.localValue !== value) {
          // keep the input set to the value before modifiers
          this.localValue = value;

          if (this.number) {
            // Emulate .number modifier behaviour
            var num = parseFloat(value);
            value = isNaN(num) ? value : num;
          } else if (this.trim) {
            // Emulate .trim modifier behaviour
            value = value.trim();
          } // Update the v-model


          this.$emit('update', value);
        }
      },
      onInput: function onInput(evt) {
        // evt.target.composing is set by Vue
        // https://github.com/vuejs/vue/blob/dev/src/platforms/web/runtime/directives/model.js
        if (evt.target.composing) {
          return;
        }

        var formatted = this.getFormatted(evt.target.value, evt);

        if (formatted === false || evt.defaultPrevented) {
          return;
        }

        this.updateValue(formatted);
        this.$emit('input', formatted);
      },
      onChange: function onChange(evt) {
        // evt.target.composing is set by Vue
        // https://github.com/vuejs/vue/blob/dev/src/platforms/web/runtime/directives/model.js
        if (evt.target.composing) {
          return;
        }

        var formatted = this.getFormatted(evt.target.value, evt);

        if (formatted === false) {
          return;
        }

        this.updateValue(formatted);
        this.$emit('change', formatted);
      },
      onBlur: function onBlur(evt) {
        // lazy formatter
        if (this.lazyFormatter) {
          var formatted = this.getFormatted(evt.target.value, evt, true);

          if (formatted === false) {
            return;
          }

          this.updateValue(formatted);
        } // Emit native blur event


        this.$emit('blur', evt);
      },
      focus: function focus() {
        // For external handler that may want a focus method
        if (!this.disabled) {
          this.$el.focus();
        }
      },
      blur: function blur() {
        // For external handler that may want a blur method
        if (!this.disabled) {
          this.$el.blur();
        }
      }
    }
  };

  // @vue/component
  var formSelectionMixin = {
    computed: {
      /* istanbul ignore next */
      selectionStart: {
        // Expose selectionStart for formatters, etc
        cache: false,
        get: function get() {
          return this.$refs.input.selectionStart;
        },
        set: function set(val) {
          this.$refs.input.selectionStart = val;
        }
      },

      /* istanbul ignore next */
      selectionEnd: {
        // Expose selectionEnd for formatters, etc
        cache: false,
        get: function get() {
          return this.$refs.input.selectionEnd;
        },
        set: function set(val) {
          this.$refs.input.selectionEnd = val;
        }
      },

      /* istanbul ignore next */
      selectionDirection: {
        // Expose selectionDirection for formatters, etc
        cache: false,
        get: function get() {
          return this.$refs.input.selectionDirection;
        },
        set: function set(val) {
          this.$refs.input.selectionDirection = val;
        }
      }
    },
    methods: {
      /* istanbul ignore next */
      select: function select() {
        var _this$$refs$input;

        // For external handler that may want a select() method
        (_this$$refs$input = this.$refs.input).select.apply(_this$$refs$input, arguments);
      },

      /* istanbul ignore next */
      setSelectionRange: function setSelectionRange() {
        var _this$$refs$input2;

        // For external handler that may want a setSelectionRange(a,b,c) method
        (_this$$refs$input2 = this.$refs.input).setSelectionRange.apply(_this$$refs$input2, arguments);
      },

      /* istanbul ignore next */
      setRangeText: function setRangeText() {
        var _this$$refs$input3;

        // For external handler that may want a setRangeText(a,b,c) method
        (_this$$refs$input3 = this.$refs.input).setRangeText.apply(_this$$refs$input3, arguments);
      }
    }
  };

  // @vue/component
  var formValidityMixin = {
    computed: {
      /* istanbul ignore next */
      validity: {
        // Expose validity property
        cache: false,
        get: function get() {
          return this.$refs.input.validity;
        }
      },

      /* istanbul ignore next */
      validationMessage: {
        // Expose validationMessage property
        cache: false,
        get: function get() {
          return this.$refs.input.validationMessage;
        }
      },

      /* istanbul ignore next */
      willValidate: {
        // Expose willValidate property
        cache: false,
        get: function get() {
          return this.$refs.input.willValidate;
        }
      }
    },
    methods: {
      /* istanbul ignore next */
      setCustomValidity: function setCustomValidity() {
        var _this$$refs$input;

        // For external handler that may want a setCustomValidity(...) method
        return (_this$$refs$input = this.$refs.input).setCustomValidity.apply(_this$$refs$input, arguments);
      },

      /* istanbul ignore next */
      checkValidity: function checkValidity() {
        var _this$$refs$input2;

        // For external handler that may want a checkValidity(...) method
        return (_this$$refs$input2 = this.$refs.input).checkValidity.apply(_this$$refs$input2, arguments);
      },

      /* istanbul ignore next */
      reportValidity: function reportValidity() {
        var _this$$refs$input3;

        // For external handler that may want a reportValidity(...) method
        return (_this$$refs$input3 = this.$refs.input).reportValidity.apply(_this$$refs$input3, arguments);
      }
    }
  };

  var TYPES = ['text', 'password', 'email', 'number', 'url', 'tel', 'search', 'range', 'color', 'date', 'time', 'datetime', 'datetime-local', 'month', 'week']; // @vue/component

  var BFormInput = {
    name: 'BFormInput',
    mixins: [idMixin, formMixin, formSizeMixin, formStateMixin, formTextMixin, formSelectionMixin, formValidityMixin],
    props: {
      value: {
        type: [String, Number],
        default: null
      },
      type: {
        type: String,
        default: 'text',
        validator: function validator(type) {
          return arrayIncludes(TYPES, type);
        }
      },
      noWheel: {
        // Disable mousewheel to prevent wheel from changing values (i.e. number/date).
        type: Boolean,
        default: false
      },
      min: {
        type: [String, Number],
        default: null
      },
      max: {
        type: [String, Number],
        default: null
      },
      step: {
        type: [String, Number],
        default: null
      }
    },
    computed: {
      localType: function localType() {
        // We only allow certain types
        return arrayIncludes(TYPES, this.type) ? this.type : 'text';
      }
    },
    watch: {
      noWheel: function noWheel(newVal) {
        this.setWheelStopper(newVal);
      }
    },
    mounted: function mounted() {
      this.setWheelStopper(this.noWheel);
    },
    deactivated: function deactivated() {
      // Turn off listeners when keep-alive component deactivated

      /* istanbul ignore next */
      this.setWheelStopper(false);
    },
    activated: function activated() {
      // Turn on listeners (if no-wheel) when keep-alive component activated

      /* istanbul ignore next */
      this.setWheelStopper(this.noWheel);
    },
    beforeDestroy: function beforeDestroy() {
      /* istanbul ignore next */
      this.setWheelStopper(false);
    },
    methods: {
      setWheelStopper: function setWheelStopper(on) {
        var input = this.$el; // We use native events, so that we don't interfere with propgation

        if (on) {
          eventOn(input, 'focus', this.onWheelFocus);
          eventOn(input, 'blur', this.onWheelBlur);
        } else {
          eventOff(input, 'focus', this.onWheelFocus);
          eventOff(input, 'blur', this.onWheelBlur);
          eventOff(document, 'wheel', this.stopWheel);
        }
      },
      onWheelFocus: function onWheelFocus(evt) {
        eventOn(document, 'wheel', this.stopWheel);
      },
      onWheelBlur: function onWheelBlur(evt) {
        eventOff(document, 'wheel', this.stopWheel);
      },
      stopWheel: function stopWheel(evt) {
        evt.preventDefault();
        this.$el.blur();
      }
    },
    render: function render(h) {
      var self = this;
      return h('input', {
        ref: 'input',
        class: self.computedClass,
        directives: [{
          name: 'model',
          rawName: 'v-model',
          value: self.localValue,
          expression: 'localValue'
        }],
        attrs: {
          id: self.safeId(),
          name: self.name,
          form: self.form || null,
          type: self.localType,
          disabled: self.disabled,
          placeholder: self.placeholder,
          required: self.required,
          autocomplete: self.autocomplete || null,
          readonly: self.readonly || self.plaintext,
          min: self.min,
          max: self.max,
          step: self.step,
          'aria-required': self.required ? 'true' : null,
          'aria-invalid': self.computedAriaInvalid
        },
        domProps: {
          value: self.localValue
        },
        on: _objectSpread({}, self.$listeners, {
          input: self.onInput,
          change: self.onChange,
          blur: self.onBlur
        })
      });
    }
  };

  var components$h = {
    BFormInput: BFormInput,
    BInput: BFormInput
  };
  var index$f = {
    install: function install(Vue) {
      registerComponents(Vue, components$h);
    }
  };

  var BFormTextarea = {
    name: 'BFormTextarea',
    mixins: [idMixin, formMixin, formSizeMixin, formStateMixin, formTextMixin, formSelectionMixin, formValidityMixin],
    props: {
      rows: {
        type: [Number, String],
        default: 2
      },
      maxRows: {
        type: [Number, String],
        default: null
      },
      wrap: {
        // 'soft', 'hard' or 'off'. Browser default is 'soft'
        type: String,
        default: 'soft'
      },
      noResize: {
        // Disable the resize handle of textarea
        type: Boolean,
        default: false
      }
    },
    data: function data() {
      return {
        dontResize: true
      };
    },
    computed: {
      computedStyle: function computedStyle() {
        return {
          // setting noResize to true will disable the ability for the user to
          // resize the textarea. We also disable when in auto resize mode
          resize: !this.computedRows || this.noResize ? 'none' : null,
          // The computed height for auto resize
          height: this.computedHeight
        };
      },
      computedMinRows: function computedMinRows() {
        // Ensure rows is at least 2 and positive (2 is the native textarea value)
        return Math.max(parseInt(this.rows, 10) || 2, 2);
      },
      computedMaxRows: function computedMaxRows() {
        return Math.max(this.computedMinRows, parseInt(this.maxRows, 10) || 0);
      },
      computedRows: function computedRows() {
        return this.computedMinRows === this.computedMaxRows ? this.computedMinRows : null;
      },
      computedHeight: function computedHeight()
      /* istanbul ignore next: can't test getComputedProperties */
      {
        var el = this.$el;

        if (this.isServer) {
          return null;
        } // We compare this.localValue to null to ensure reactivity of content changes.


        if (this.localValue === null || this.computedRows || this.dontResize || this.$isServer) {
          return null;
        } // Element must be visible (not hidden) and in document. *Must* be checked after above.


        if (!isVisible(el)) {
          return null;
        } // Remember old height and reset it temporarily


        var oldHeight = el.style.height;
        el.style.height = 'auto'; // Get current computed styles

        var computedStyle = getCS(el); // Height of one line of text in px

        var lineHeight = parseFloat(computedStyle.lineHeight); // Minimum height for min rows (browser dependant)

        var minHeight = parseInt(computedStyle.height, 10) || lineHeight * this.computedMinRows; // Calculate height of content

        var offset = (parseFloat(computedStyle.borderTopWidth) || 0) + (parseFloat(computedStyle.borderBottomWidth) || 0) + (parseFloat(computedStyle.paddingTop) || 0) + (parseFloat(computedStyle.paddingBottom) || 0); // Calculate content height in "rows"

        var contentRows = (el.scrollHeight - offset) / lineHeight; // Put the old height back (needed when new height is equal to old height!)

        el.style.height = oldHeight; // Calculate number of rows to display (limited within min/max rows)

        var rows = Math.min(Math.max(contentRows, this.computedMinRows), this.computedMaxRows); // Calulate the required height of the textarea including border and padding (in pixels)

        var height = Math.max(Math.ceil(rows * lineHeight + offset), minHeight); // return the new computed height in px units

        return "".concat(height, "px");
      }
    },
    mounted: function mounted() {
      var _this = this;

      // Enable opt-in resizing once mounted
      this.$nextTick(function () {
        _this.dontResize = false;
      });
    },
    activated: function activated() {
      var _this2 = this;

      // If we are being re-activated in <keep-alive>, enable opt-in resizing
      this.$nextTick(function () {
        _this2.dontResize = false;
      });
    },
    deactivated: function deactivated() {
      // If we are in a deactivated <keep-alive>, disable opt-in resizing
      this.dontResize = true;
    },
    beforeDestroy: function beforeDestroy() {
      /* istanbul ignore next */
      this.dontResize = true;
    },
    render: function render(h) {
      // Using self instead of this helps reduce code size during minification
      var self = this;
      return h('textarea', {
        ref: 'input',
        class: self.computedClass,
        style: self.computedStyle,
        directives: [{
          name: 'model',
          rawName: 'v-model',
          value: self.localValue,
          expression: 'localValue'
        }],
        attrs: {
          id: self.safeId(),
          name: self.name,
          form: self.form || null,
          disabled: self.disabled,
          placeholder: self.placeholder,
          required: self.required,
          autocomplete: self.autocomplete || null,
          readonly: self.readonly || self.plaintext,
          rows: self.computedRows,
          wrap: self.wrap || null,
          'aria-required': self.required ? 'true' : null,
          'aria-invalid': self.computedAriaInvalid
        },
        domProps: {
          value: self.localValue
        },
        on: _objectSpread({}, self.$listeners, {
          input: self.onInput,
          change: self.onChange,
          blur: self.onBlur
        })
      });
    }
  };

  var components$i = {
    BFormTextarea: BFormTextarea,
    BTextarea: BFormTextarea
  };
  var index$g = {
    install: function install(Vue) {
      registerComponents(Vue, components$i);
    }
  };

  // @vue/component
  var formCustomMixin = {
    props: {
      plain: {
        type: Boolean,
        default: false
      }
    },
    computed: {
      custom: function custom() {
        return !this.plain;
      }
    }
  };

  var BFormFile = {
    name: 'BFormFile',
    mixins: [idMixin, formMixin, formStateMixin, formCustomMixin],
    props: {
      value: {
        // type: Object,
        default: null
      },
      accept: {
        type: String,
        default: ''
      },
      // Instruct input to capture from camera
      capture: {
        type: Boolean,
        default: false
      },
      placeholder: {
        type: String,
        default: 'No file chosen' // Chrome default file prompt

      },
      browseText: {
        type: String,
        default: null
      },
      dropPlaceholder: {
        type: String,
        default: null
      },
      multiple: {
        type: Boolean,
        default: false
      },
      directory: {
        type: Boolean,
        default: false
      },
      noTraverse: {
        type: Boolean,
        default: false
      },
      noDrop: {
        type: Boolean,
        default: false
      }
    },
    data: function data() {
      return {
        selectedFile: null,
        dragging: false,
        hasFocus: false
      };
    },
    computed: {
      selectLabel: function selectLabel() {
        // Draging active
        if (this.dragging && this.dropPlaceholder) {
          return this.dropPlaceholder;
        } // No file choosen


        if (!this.selectedFile || this.selectedFile.length === 0) {
          return this.placeholder;
        } // Multiple files


        if (this.multiple) {
          if (this.selectedFile.length === 1) {
            return this.selectedFile[0].name;
          }

          return this.selectedFile.map(function (file) {
            return file.name;
          }).join(', ');
        } // Single file


        return this.selectedFile.name;
      }
    },
    watch: {
      selectedFile: function selectedFile(newVal, oldVal) {
        if (looseEqual(newVal, oldVal)) {
          return;
        }

        if (!newVal && this.multiple) {
          this.$emit('input', []);
        } else {
          this.$emit('input', newVal);
        }
      },
      value: function value(newVal) {
        if (!newVal || isArray(newVal) && newVal.length === 0) {
          this.reset();
        }
      }
    },
    methods: {
      focusHandler: function focusHandler(evt) {
        // Bootstrap v4.beta doesn't have focus styling for custom file input
        // Firefox has a borked '[type=file]:focus ~ sibling' selector issue,
        // So we add a 'focus' class to get around these "bugs"
        if (this.plain || evt.type === 'focusout') {
          this.hasFocus = false;
        } else {
          // Add focus styling for custom file input
          this.hasFocus = true;
        }
      },
      reset: function reset() {
        try {
          // Wrapped in try in case IE < 11 craps out
          this.$refs.input.value = '';
        } catch (e) {} // IE < 11 doesn't support setting input.value to '' or null
        // So we use this little extra hack to reset the value, just in case
        // This also appears to work on modern browsers as well.


        this.$refs.input.type = '';
        this.$refs.input.type = 'file';
        this.selectedFile = this.multiple ? [] : null;
      },
      onFileChange: function onFileChange(evt) {
        var _this = this;

        // Always emit original event
        this.$emit('change', evt); // Check if special `items` prop is available on event (drop mode)
        // Can be disabled by setting no-traverse

        var items = evt.dataTransfer && evt.dataTransfer.items;

        if (items && !this.noTraverse) {
          var queue = [];

          for (var i = 0; i < items.length; i++) {
            var item = items[i].webkitGetAsEntry();

            if (item) {
              queue.push(this.traverseFileTree(item));
            }
          }

          Promise.all(queue).then(function (filesArr) {
            _this.setFiles(from(filesArr));
          });
          return;
        } // Normal handling


        this.setFiles(evt.target.files || evt.dataTransfer.files);
      },
      setFiles: function setFiles(files) {
        if (!files) {
          this.selectedFile = null;
        } else if (this.multiple) {
          // Convert files to array
          var filesArray = [];

          for (var i = 0; i < files.length; i++) {
            filesArray.push(files[i]);
          } // Return file(s) as array


          this.selectedFile = filesArray;
        } else {
          // Return single file object
          this.selectedFile = files[0];
        }
      },
      onReset: function onReset() {
        // Triggered when the parent form (if any) is reset
        this.selectedFile = this.multiple ? [] : null;
      },
      onDragover: function onDragover(evt) {
        evt.preventDefault();
        evt.stopPropagation();

        if (this.noDrop || !this.custom) {
          return;
        }

        this.dragging = true;
        evt.dataTransfer.dropEffect = 'copy';
      },
      onDragleave: function onDragleave(evt) {
        evt.preventDefault();
        evt.stopPropagation();
        this.dragging = false;
      },
      onDrop: function onDrop(evt) {
        evt.preventDefault();
        evt.stopPropagation();

        if (this.noDrop) {
          return;
        }

        this.dragging = false;

        if (evt.dataTransfer.files && evt.dataTransfer.files.length > 0) {
          this.onFileChange(evt);
        }
      },
      traverseFileTree: function traverseFileTree(item, path) {
        var _this2 = this;

        // Based on http://stackoverflow.com/questions/3590058
        return new Promise(function (resolve) {
          path = path || '';

          if (item.isFile) {
            // Get file
            item.file(function (file) {
              file.$path = path; // Inject $path to file obj

              resolve(file);
            });
          } else if (item.isDirectory) {
            // Get folder contents
            item.createReader().readEntries(function (entries) {
              var queue = [];

              for (var i = 0; i < entries.length; i++) {
                queue.push(_this2.traverseFileTree(entries[i], path + item.name + '/'));
              }

              Promise.all(queue).then(function (filesArr) {
                resolve(from(filesArr));
              });
            });
          }
        });
      }
    },
    render: function render(h) {
      // Form Input
      var input = h('input', {
        ref: 'input',
        class: [{
          'form-control-file': this.plain,
          'custom-file-input': this.custom,
          focus: this.custom && this.hasFocus
        }, this.stateClass],
        attrs: {
          type: 'file',
          id: this.safeId(),
          name: this.name,
          disabled: this.disabled,
          required: this.required,
          form: this.form || null,
          capture: this.capture || null,
          accept: this.accept || null,
          multiple: this.multiple,
          webkitdirectory: this.directory,
          'aria-required': this.required ? 'true' : null
        },
        on: {
          change: this.onFileChange,
          focusin: this.focusHandler,
          focusout: this.focusHandler,
          reset: this.onReset
        }
      });

      if (this.plain) {
        return input;
      } // Overlay Labels


      var label = h('label', {
        class: ['custom-file-label', this.dragging ? 'dragging' : null],
        attrs: {
          for: this.safeId(),
          'data-browse': this.browseText || null
        }
      }, this.selectLabel); // Return rendered custom file input

      return h('div', {
        class: ['custom-file', 'b-form-file', this.stateClass],
        attrs: {
          id: this.safeId('_BV_file_outer_')
        },
        on: {
          dragover: this.onDragover,
          dragleave: this.onDragleave,
          drop: this.onDrop
        }
      }, [input, label]);
    }
  };

  var components$j = {
    BFormFile: BFormFile,
    BFile: BFormFile
  };
  var index$h = {
    install: function install(Vue) {
      registerComponents(Vue, components$j);
    }
  };

  var BFormSelect = {
    name: 'BFormSelect',
    mixins: [idMixin, formMixin, formSizeMixin, formStateMixin, formCustomMixin, formOptionsMixin],
    props: {
      value: {// type: Object,
        // default: undefined
      },
      multiple: {
        type: Boolean,
        default: false
      },
      selectSize: {
        // Browsers default size to 0, which shows 4 rows in most browsers in multiple mode
        // Size of 1 can bork out Firefox
        type: Number,
        default: 0
      },
      ariaInvalid: {
        type: [Boolean, String],
        default: false
      }
    },
    data: function data() {
      return {
        localValue: this.value
      };
    },
    computed: {
      computedSelectSize: function computedSelectSize() {
        // Custom selects with a size of zero causes the arrows to be hidden,
        // so dont render the size attribute in this case
        return !this.plain && this.selectSize === 0 ? null : this.selectSize;
      },
      inputClass: function inputClass() {
        return [this.plain ? 'form-control' : 'custom-select', this.size && this.plain ? "form-control-".concat(this.size) : null, this.size && !this.plain ? "custom-select-".concat(this.size) : null, this.stateClass];
      },
      computedAriaInvalid: function computedAriaInvalid() {
        if (this.ariaInvalid === true || this.ariaInvalid === 'true') {
          return 'true';
        }

        return this.stateClass === 'is-invalid' ? 'true' : null;
      }
    },
    watch: {
      value: function value(newVal, oldVal) {
        this.localValue = newVal;
      },
      localValue: function localValue(newVal, oldVal) {
        this.$emit('input', this.localValue);
      }
    },
    methods: {
      focus: function focus() {
        this.$refs.input.focus();
      },
      blur: function blur() {
        this.$refs.input.blur();
      }
    },
    render: function render(h) {
      var _this = this;

      var $slots = this.$slots;
      var options = this.formOptions.map(function (option, index) {
        return h('option', {
          key: "option_".concat(index, "_opt"),
          attrs: {
            disabled: Boolean(option.disabled)
          },
          domProps: _objectSpread({}, htmlOrText(option.html, option.text), {
            value: option.value
          })
        });
      });
      return h('select', {
        ref: 'input',
        class: this.inputClass,
        directives: [{
          name: 'model',
          rawName: 'v-model',
          value: this.localValue,
          expression: 'localValue'
        }],
        attrs: {
          id: this.safeId(),
          name: this.name,
          form: this.form || null,
          multiple: this.multiple || null,
          size: this.computedSelectSize,
          disabled: this.disabled,
          required: this.required,
          'aria-required': this.required ? 'true' : null,
          'aria-invalid': this.computedAriaInvalid
        },
        on: {
          change: function change(evt) {
            var target = evt.target;
            var selectedVal = from(target.options).filter(function (o) {
              return o.selected;
            }).map(function (o) {
              return '_value' in o ? o._value : o.value;
            });
            _this.localValue = target.multiple ? selectedVal : selectedVal[0];

            _this.$nextTick(function () {
              _this.$emit('change', _this.localValue);
            });
          }
        }
      }, [$slots.first, options, $slots.default]);
    }
  };

  var components$k = {
    BFormSelect: BFormSelect,
    BSelect: BFormSelect
  };
  var index$i = {
    install: function install(Vue) {
      registerComponents(Vue, components$k);
    }
  };

  var THROTTLE = 100;
  var EventOptions$2 = {
    passive: true,
    capture: false // @vue/component

  };
  var BImgLazy = {
    name: 'BImgLazy',
    components: {
      BImg: BImg
    },
    props: {
      src: {
        type: String,
        default: null,
        required: true
      },
      alt: {
        type: String,
        default: null
      },
      width: {
        type: [Number, String],
        default: null
      },
      height: {
        type: [Number, String],
        default: null
      },
      blankSrc: {
        // If null, a blank image is generated
        type: String,
        default: null
      },
      blankColor: {
        type: String,
        default: 'transparent'
      },
      blankWidth: {
        type: [Number, String],
        default: null
      },
      blankHeight: {
        type: [Number, String],
        default: null
      },
      show: {
        type: Boolean,
        default: false
      },
      fluid: {
        type: Boolean,
        default: false
      },
      fluidGrow: {
        type: Boolean,
        default: false
      },
      block: {
        type: Boolean,
        default: false
      },
      thumbnail: {
        type: Boolean,
        default: false
      },
      rounded: {
        type: [Boolean, String],
        default: false
      },
      left: {
        type: Boolean,
        default: false
      },
      right: {
        type: Boolean,
        default: false
      },
      center: {
        type: Boolean,
        default: false
      },
      offset: {
        type: [Number, String],
        default: 360
      },
      throttle: {
        type: [Number, String],
        default: THROTTLE
      }
    },
    data: function data() {
      return {
        isShown: false,
        scrollTimeout: null
      };
    },
    computed: {
      computedSrc: function computedSrc() {
        return !this.blankSrc || this.isShown ? this.src : this.blankSrc;
      },
      computedBlank: function computedBlank() {
        return !(this.isShown || this.blankSrc);
      },
      computedWidth: function computedWidth() {
        return this.isShown ? this.width : this.blankWidth || this.width;
      },
      computedHeight: function computedHeight() {
        return this.isShown ? this.height : this.blankHeight || this.height;
      }
    },
    watch: {
      show: function show(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.isShown = newVal;

          if (!newVal) {
            // Make sure listeners are re-enabled if img is force set to blank
            this.setListeners(true);
          }
        }
      },
      isShown: function isShown(newVal, oldVal) {
        if (newVal !== oldVal) {
          // Update synched show prop
          this.$emit('update:show', newVal);
        }
      }
    },
    created: function created() {
      this.isShown = this.show;
    },
    mounted: function mounted() {
      if (this.isShown) {
        this.setListeners(false);
      } else {
        this.setListeners(true);
        this.$nextTick(this.checkView);
      }
    },
    activated: function activated() {
      /* istanbul ignore if */
      if (!this.isShown) {
        this.setListeners(true);
        this.$nextTick(this.checkView);
      }
    },
    deactivated: function deactivated() {
      /* istanbul ignore next */
      this.setListeners(false);
    },
    beforeDestroy: function beforeDestroy() {
      /* istanbul ignore next */
      this.setListeners(false);
    },
    methods: {
      setListeners: function setListeners(on) {
        clearTimeout(this.scrollTimer);
        this.scrollTimeout = null;
        var root = window;

        if (on) {
          eventOn(this.$el, 'load', this.checkView);
          eventOn(root, 'scroll', this.onScroll, EventOptions$2);
          eventOn(root, 'resize', this.onScroll, EventOptions$2);
          eventOn(root, 'orientationchange', this.onScroll, EventOptions$2);
          eventOn(document, 'transitionend', this.onScroll, EventOptions$2);
        } else {
          eventOff(this.$el, 'load', this.checkView);
          eventOff(root, 'scroll', this.onScroll, EventOptions$2);
          eventOff(root, 'resize', this.onScroll, EventOptions$2);
          eventOff(root, 'orientationchange', this.onScroll, EventOptions$2);
          eventOff(document, 'transitionend', this.onScroll, EventOptions$2);
        }
      },
      checkView: function checkView()
      /* istanbul ignore next: can't test getBoundingClientRect in JSDOM */
      {
        // check bounding box + offset to see if we should show
        if (this.isShown) {
          this.setListeners(false);
          return;
        }

        var offset = parseInt(this.offset, 10) || 0;
        var docElement = document.documentElement;
        var view = {
          l: 0 - offset,
          t: 0 - offset,
          b: docElement.clientHeight + offset,
          r: docElement.clientWidth + offset
          /* istanbul ignore next */

        };
        var box = getBCR(this.$el);
        /* istanbul ignore if */

        if (box.right >= view.l && box.bottom >= view.t && box.left <= view.r && box.top <= view.b) {
          // image is in view (or about to be in view)
          this.isShown = true;
          this.setListeners(false);
        }
      },
      onScroll: function onScroll() {
        if (this.isShown) {
          this.setListeners(false);
        } else {
          clearTimeout(this.scrollTimeout);
          this.scrollTimeout = setTimeout(this.checkView, parseInt(this.throttle, 10) || THROTTLE);
        }
      }
    },
    render: function render(h) {
      return h('b-img', {
        props: {
          src: this.computedSrc,
          alt: this.alt,
          blank: this.computedBlank,
          blankColor: this.blankColor,
          width: this.computedWidth,
          height: this.computedHeight,
          fluid: this.fluid,
          fluidGrow: this.fluidGrow,
          block: this.block,
          thumbnail: this.thumbnail,
          rounded: this.rounded,
          left: this.left,
          right: this.right,
          center: this.center
        }
      });
    }
  };

  var components$l = {
    BImg: BImg,
    BImgLazy: BImgLazy
  };
  var index$j = {
    install: function install(Vue) {
      registerComponents(Vue, components$l);
    }
  };

  var props$v = {
    fluid: {
      type: Boolean,
      default: false
    },
    containerFluid: {
      type: Boolean,
      default: false
    },
    header: {
      type: String,
      default: null
    },
    headerHtml: {
      type: String,
      default: null
    },
    headerTag: {
      type: String,
      default: 'h1'
    },
    headerLevel: {
      type: [Number, String],
      default: '3'
    },
    lead: {
      type: String,
      default: null
    },
    leadHtml: {
      type: String,
      default: null
    },
    leadTag: {
      type: String,
      default: 'p'
    },
    tag: {
      type: String,
      default: 'div'
    },
    bgVariant: {
      type: String,
      default: null
    },
    borderVariant: {
      type: String,
      default: null
    },
    textVariant: {
      type: String,
      default: null
    } // @vue/component

  };
  var BJumbotron = {
    name: 'BJumbotron',
    functional: true,
    props: props$v,
    render: function render(h, _ref) {
      var _class2;

      var props = _ref.props,
          data = _ref.data,
          slots = _ref.slots;
      // The order of the conditionals matter.
      // We are building the component markup in order.
      var childNodes = [];
      var $slots = slots(); // Header

      if (props.header || $slots.header || props.headerHtml) {
        childNodes.push(h(props.headerTag, {
          class: _defineProperty({}, "display-".concat(props.headerLevel), Boolean(props.headerLevel))
        }, $slots.header || props.headerHtml || stripTags(props.header)));
      } // Lead


      if (props.lead || $slots.lead || props.leadHtml) {
        childNodes.push(h(props.leadTag, {
          staticClass: 'lead'
        }, $slots.lead || props.leadHtml || stripTags(props.lead)));
      } // Default slot


      if ($slots.default) {
        childNodes.push($slots.default);
      } // If fluid, wrap content in a container/container-fluid


      if (props.fluid) {
        // Children become a child of a container
        childNodes = [h(Container, {
          props: {
            fluid: props.containerFluid
          }
        }, childNodes)];
      } // Return the jumbotron


      return h(props.tag, mergeData(data, {
        staticClass: 'jumbotron',
        class: (_class2 = {
          'jumbotron-fluid': props.fluid
        }, _defineProperty(_class2, "text-".concat(props.textVariant), Boolean(props.textVariant)), _defineProperty(_class2, "bg-".concat(props.bgVariant), Boolean(props.bgVariant)), _defineProperty(_class2, "border-".concat(props.borderVariant), Boolean(props.borderVariant)), _defineProperty(_class2, "border", Boolean(props.borderVariant)), _class2)
      }), childNodes);
    }
  };

  var components$m = {
    BJumbotron: BJumbotron
  };
  var index$k = {
    install: function install(Vue) {
      registerComponents(Vue, components$m);
    }
  };

  var components$n = {
    BLink: BLink
  };
  var index$l = {
    install: function install(Vue) {
      registerComponents(Vue, components$n);
    }
  };

  var props$w = {
    tag: {
      type: String,
      default: 'div'
    },
    flush: {
      type: Boolean,
      default: false
    },
    horizontal: {
      type: [Boolean, String],
      default: false
    } // @vue/component

  };
  var BListGroup = {
    name: 'BListGroup',
    functional: true,
    props: props$w,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var horizontal = props.horizontal === '' ? true : props.horizontal;
      horizontal = props.flush ? false : horizontal;
      var componentData = {
        staticClass: 'list-group',
        class: _defineProperty({
          'list-group-flush': props.flush,
          'list-group-horizontal': horizontal === true
        }, "list-group-horizontal-".concat(horizontal), typeof horizontal === 'string')
      };
      return h(props.tag, mergeData(data, componentData), children);
    }
  };

  var actionTags = ['a', 'router-link', 'button', 'b-link'];
  var linkProps$2 = propsFactory();
  delete linkProps$2.href.default;
  delete linkProps$2.to.default;
  var props$x = _objectSpread({
    tag: {
      type: String,
      default: 'div'
    },
    action: {
      type: Boolean,
      default: null
    },
    button: {
      type: Boolean,
      default: null
    },
    variant: {
      type: String,
      default: null
    }
  }, linkProps$2); // @vue/component

  var BListGroupItem = {
    name: 'BListGroupItem',
    functional: true,
    props: props$x,
    render: function render(h, _ref) {
      var _class;

      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var tag = props.button ? 'button' : !props.href && !props.to ? props.tag : BLink;
      var isAction = Boolean(props.href || props.to || props.action || props.button || arrayIncludes(actionTags, props.tag));
      var attrs = {};
      var itemProps = {};

      if (tag === 'button') {
        if (!data.attrs || !data.attrs.type) {
          // Add a type for button is one not provided in passed attributes
          attrs.type = 'button';
        }

        if (props.disabled) {
          // Set disabled attribute if button and disabled
          attrs.disabled = true;
        }
      } else {
        itemProps = pluckProps(linkProps$2, props);
      }

      var componentData = {
        attrs: attrs,
        props: itemProps,
        staticClass: 'list-group-item',
        class: (_class = {}, _defineProperty(_class, "list-group-item-".concat(props.variant), Boolean(props.variant)), _defineProperty(_class, 'list-group-item-action', isAction), _defineProperty(_class, "active", props.active), _defineProperty(_class, "disabled", props.disabled), _class)
      };
      return h(tag, mergeData(data, componentData), children);
    }
  };

  var components$o = {
    BListGroup: BListGroup,
    BListGroupItem: BListGroupItem
  };
  var index$m = {
    install: function install(Vue) {
      registerComponents(Vue, components$o);
    }
  };

  var props$y = {
    tag: {
      type: String,
      default: 'div'
    }
  };
  var BMediaBody = {
    name: 'BMediaBody',
    functional: true,
    props: props$y,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        staticClass: 'media-body'
      }), children);
    }
  };

  var props$z = {
    tag: {
      type: String,
      default: 'div'
    },
    verticalAlign: {
      type: String,
      default: 'top'
    } // @vue/component

  };
  var BMediaAside = {
    name: 'BMediaAside',
    functional: true,
    props: props$z,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        staticClass: 'd-flex',
        class: _defineProperty({}, "align-self-".concat(props.verticalAlign), props.verticalAlign)
      }), children);
    }
  };

  var props$A = {
    tag: {
      type: String,
      default: 'div'
    },
    rightAlign: {
      type: Boolean,
      default: false
    },
    verticalAlign: {
      type: String,
      default: 'top'
    },
    noBody: {
      type: Boolean,
      default: false
    } // @vue/component

  };
  var BMedia = {
    name: 'BMedia',
    functional: true,
    props: props$A,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          slots = _ref.slots,
          children = _ref.children;
      var childNodes = props.noBody ? children : [];
      var $slots = slots();

      if (!props.noBody) {
        if ($slots.aside && !props.rightAlign) {
          childNodes.push(h(BMediaAside, {
            staticClass: 'mr-3',
            props: {
              verticalAlign: props.verticalAlign
            }
          }, $slots.aside));
        }

        childNodes.push(h(BMediaBody, $slots.default));

        if ($slots.aside && props.rightAlign) {
          childNodes.push(h(BMediaAside, {
            staticClass: 'ml-3',
            props: {
              verticalAlign: props.verticalAlign
            }
          }, $slots.aside));
        }
      }

      return h(props.tag, mergeData(data, {
        staticClass: 'media'
      }), childNodes);
    }
  };

  var components$p = {
    BMedia: BMedia,
    BMediaAside: BMediaAside,
    BMediaBody: BMediaBody
  };
  var index$n = {
    install: function install(Vue) {
      registerComponents(Vue, components$p);
    }
  };

  var Selector$1 = {
    FIXED_CONTENT: '.fixed-top, .fixed-bottom, .is-fixed, .sticky-top',
    STICKY_CONTENT: '.sticky-top',
    NAVBAR_TOGGLER: '.navbar-toggler' // ObserveDom config

  };
  var OBSERVER_CONFIG = {
    subtree: true,
    childList: true,
    characterData: true,
    attributes: true,
    attributeFilter: ['style', 'class'] // modal wrapper ZINDEX offset incrememnt

  };
  var ZINDEX_OFFSET = 2000; // Modal open count helpers

  function getModalOpenCount() {
    return parseInt(getAttr(document.body, 'data-modal-open-count') || 0, 10);
  }

  function setModalOpenCount(count) {
    setAttr(document.body, 'data-modal-open-count', String(count));
    return count;
  }

  function incrementModalOpenCount() {
    return setModalOpenCount(getModalOpenCount() + 1);
  }

  function decrementModalOpenCount() {
    return setModalOpenCount(Math.max(getModalOpenCount() - 1, 0));
  } // Returns the current visible modal highest z-index


  function getModalMaxZIndex() {
    return selectAll('div.modal')
    /* find all modals that are in document */
    .filter(isVisible)
    /* filter only visible ones */
    .map(function (m) {
      return m.parentElement;
    })
    /* select the outer div */
    .reduce(function (max, el) {
      /* compute the highest z-index */
      return Math.max(max, parseInt(el.style.zIndex || 0, 10));
    }, 0);
  } // Returns the next z-index to be used by a modal to ensure proper stacking
  // regardless of document order. Increments by 2000


  function getModalNextZIndex() {
    return getModalMaxZIndex() + ZINDEX_OFFSET;
  } // @vue/component


  var BModal = {
    name: 'BModal',
    components: {
      BButton: BButton,
      BButtonClose: BButtonClose
    },
    mixins: [idMixin, listenOnRootMixin],
    model: {
      prop: 'visible',
      event: 'change'
    },
    props: {
      title: {
        type: String,
        default: ''
      },
      titleHtml: {
        type: String
      },
      titleTag: {
        type: String,
        default: 'h5'
      },
      size: {
        type: String,
        default: 'md'
      },
      centered: {
        type: Boolean,
        default: false
      },
      scrollable: {
        type: Boolean,
        default: false
      },
      buttonSize: {
        type: String,
        default: ''
      },
      noStacking: {
        type: Boolean,
        default: false
      },
      noFade: {
        type: Boolean,
        default: false
      },
      noCloseOnBackdrop: {
        type: Boolean,
        default: false
      },
      noCloseOnEsc: {
        type: Boolean,
        default: false
      },
      noEnforceFocus: {
        type: Boolean,
        default: false
      },
      headerBgVariant: {
        type: String,
        default: null
      },
      headerBorderVariant: {
        type: String,
        default: null
      },
      headerTextVariant: {
        type: String,
        default: null
      },
      headerClass: {
        type: [String, Array],
        default: null
      },
      bodyBgVariant: {
        type: String,
        default: null
      },
      bodyTextVariant: {
        type: String,
        default: null
      },
      modalClass: {
        type: [String, Array],
        default: null
      },
      dialogClass: {
        type: [String, Array],
        default: null
      },
      contentClass: {
        type: [String, Array],
        default: null
      },
      bodyClass: {
        type: [String, Array],
        default: null
      },
      footerBgVariant: {
        type: String,
        default: null
      },
      footerBorderVariant: {
        type: String,
        default: null
      },
      footerTextVariant: {
        type: String,
        default: null
      },
      footerClass: {
        type: [String, Array],
        default: null
      },
      hideHeader: {
        type: Boolean,
        default: false
      },
      hideFooter: {
        type: Boolean,
        default: false
      },
      hideHeaderClose: {
        type: Boolean,
        default: false
      },
      hideBackdrop: {
        type: Boolean,
        default: false
      },
      okOnly: {
        type: Boolean,
        default: false
      },
      okDisabled: {
        type: Boolean,
        default: false
      },
      cancelDisabled: {
        type: Boolean,
        default: false
      },
      visible: {
        type: Boolean,
        default: false
      },
      returnFocus: {
        // type: Object,
        default: null
      },
      headerCloseLabel: {
        type: String,
        default: 'Close'
      },
      cancelTitle: {
        type: String,
        default: 'Cancel'
      },
      cancelTitleHtml: {
        type: String
      },
      okTitle: {
        type: String,
        default: 'OK'
      },
      okTitleHtml: {
        type: String
      },
      cancelVariant: {
        type: String,
        default: 'secondary'
      },
      okVariant: {
        type: String,
        default: 'primary'
      },
      lazy: {
        type: Boolean,
        default: false
      },
      busy: {
        type: Boolean,
        default: false
      }
    },
    data: function data() {
      return {
        is_hidden: this.lazy || false,
        // for lazy modals
        is_visible: false,
        // controls modal visible state
        is_transitioning: false,
        // Used for style control
        is_show: false,
        // Used for style control
        is_block: false,
        // Used for style control
        is_opening: false,
        // Semaphore for previnting incorrect modal open counts
        is_closing: false,
        // Semapbore for preventing incorrect modal open counts
        scrollbarWidth: 0,
        zIndex: ZINDEX_OFFSET,
        // z-index for modal stacking
        isTop: true,
        // If the modal is the topmost opened modal
        isBodyOverflowing: false,
        return_focus: this.returnFocus || null
      };
    },
    computed: {
      contentClasses: function contentClasses() {
        return ['modal-content', this.contentClass];
      },
      modalClasses: function modalClasses() {
        return [{
          fade: !this.noFade,
          show: this.is_show,
          'd-block': this.is_block
        }, this.modalClass];
      },
      dialogClasses: function dialogClasses() {
        var _ref;

        return [(_ref = {}, _defineProperty(_ref, "modal-".concat(this.size), Boolean(this.size)), _defineProperty(_ref, 'modal-dialog-centered', this.centered), _defineProperty(_ref, 'modal-dialog-scrollable', this.scrollable), _ref), this.dialogClass];
      },
      backdropClasses: function backdropClasses() {
        return {
          fade: !this.noFade,
          show: this.is_show || this.noFade
        };
      },
      headerClasses: function headerClasses() {
        var _ref2;

        return [(_ref2 = {}, _defineProperty(_ref2, "bg-".concat(this.headerBgVariant), Boolean(this.headerBgVariant)), _defineProperty(_ref2, "text-".concat(this.headerTextVariant), Boolean(this.headerTextVariant)), _defineProperty(_ref2, "border-".concat(this.headerBorderVariant), Boolean(this.headerBorderVariant)), _ref2), this.headerClass];
      },
      bodyClasses: function bodyClasses() {
        var _ref3;

        return [(_ref3 = {}, _defineProperty(_ref3, "bg-".concat(this.bodyBgVariant), Boolean(this.bodyBgVariant)), _defineProperty(_ref3, "text-".concat(this.bodyTextVariant), Boolean(this.bodyTextVariant)), _ref3), this.bodyClass];
      },
      footerClasses: function footerClasses() {
        var _ref4;

        return [(_ref4 = {}, _defineProperty(_ref4, "bg-".concat(this.footerBgVariant), Boolean(this.footerBgVariant)), _defineProperty(_ref4, "text-".concat(this.footerTextVariant), Boolean(this.footerTextVariant)), _defineProperty(_ref4, "border-".concat(this.footerBorderVariant), Boolean(this.footerBorderVariant)), _ref4), this.footerClass];
      },
      modalOuterStyle: function modalOuterStyle() {
        return {
          // We only set these styles on the stacked modals (ones with next z-index > 0).
          position: 'relative',
          zIndex: this.zIndex
        };
      }
    },
    watch: {
      visible: function visible(newVal, oldVal) {
        if (newVal === oldVal) {
          return;
        }

        this[newVal ? 'show' : 'hide']();
      }
    },
    created: function created() {
      // create non-reactive property
      this._observer = null;
    },
    mounted: function mounted() {
      // Listen for events from others to either open or close ourselves
      // And listen to all modals to enable/disable enforce focus
      this.listenOnRoot('bv::show::modal', this.showHandler);
      this.listenOnRoot('bv::modal::shown', this.shownHandler);
      this.listenOnRoot('bv::hide::modal', this.hideHandler);
      this.listenOnRoot('bv::modal::hidden', this.hiddenHandler); // Listen for bv:modal::show events, and close ourselves if the opening modal not us

      this.listenOnRoot('bv::modal::show', this.modalListener); // Initially show modal?

      if (this.visible === true) {
        this.show();
      }
    },
    beforeDestroy: function beforeDestroy()
    /* instanbul ignore next */
    {
      // Ensure everything is back to normal
      if (this._observer) {
        this._observer.disconnect();

        this._observer = null;
      } // Ensure our root "once" listener is gone


      this.$root.$off('bv::modal::hidden', this.doShow);
      this.setEnforceFocus(false);
      this.setResizeEvent(false);

      if (this.is_visible) {
        this.is_visible = false;
        this.is_show = false;
        this.is_transitioning = false;
        var count = decrementModalOpenCount();

        if (count === 0) {
          // Re-adjust body/navbar/fixed padding/margins (as we were the last modal open)
          this.setModalOpenClass(false);
          this.resetScrollbar();
          this.resetDialogAdjustments();
        }
      }
    },
    methods: {
      // Public Methods
      show: function show() {
        if (this.is_visible || this.is_opening) {
          // if already open, on in the process of opening, do nothing
          return;
        }

        if (this.is_closing) {
          // if we are in the process of closing, wait until hidden before re-opening
          this.$once('hidden', this.show);
          return;
        }

        this.is_opening = true;
        var showEvt = new BvEvent('show', {
          cancelable: true,
          vueTarget: this,
          target: this.$refs.modal,
          modalId: this.safeId(),
          relatedTarget: null
        });
        this.emitEvent(showEvt); // Don't show if canceled

        if (showEvt.defaultPrevented || this.is_visible) {
          this.is_opening = false;
          return;
        }

        if (!this.noStacking) {
          // Find the z-index to use
          this.zIndex = getModalNextZIndex(); // Show the modal

          this.doShow();
          return;
        }

        if (hasClass(document.body, 'modal-open')) {
          // If another modal is already open, wait for it to close
          this.$root.$once('bv::modal::hidden', this.doShow);
          return;
        } // Show the modal


        this.doShow();
      },
      hide: function hide(trigger) {
        if (!this.is_visible || this.is_closing) {
          return;
        }

        this.is_closing = true;
        var hideEvt = new BvEvent('hide', {
          cancelable: true,
          vueTarget: this,
          target: this.$refs.modal,
          modalId: this.safeId(),
          // this could be the trigger element/component reference
          relatedTarget: null,
          isOK: trigger || null,
          trigger: trigger || null,
          cancel: function cancel() {
            // Backwards compatibility
            warn('b-modal: evt.cancel() is deprecated. Please use evt.preventDefault().');
            this.preventDefault();
          }
        });

        if (trigger === 'ok') {
          this.$emit('ok', hideEvt);
        } else if (trigger === 'cancel') {
          this.$emit('cancel', hideEvt);
        }

        this.emitEvent(hideEvt); // Hide if not canceled

        if (hideEvt.defaultPrevented || !this.is_visible) {
          this.is_closing = false;
          return;
        } // stop observing for content changes


        if (this._observer) {
          this._observer.disconnect();

          this._observer = null;
        }

        this.is_visible = false;
        this.$emit('change', false);
      },
      // Private method to finish showing modal
      doShow: function doShow() {
        var _this = this;

        // Place modal in DOM if lazy
        this.is_hidden = false;
        this.$nextTick(function () {
          // We do this in nextTick to ensure the modal is in DOM first before we show it
          _this.is_visible = true;
          _this.is_opening = false;

          _this.$emit('change', true); // Observe changes in modal content and adjust if necessary


          _this._observer = observeDOM(_this.$refs.content, _this.adjustDialog.bind(_this), OBSERVER_CONFIG);
        });
      },
      // Transition Handlers
      onBeforeEnter: function onBeforeEnter() {
        this.getScrollbarWidth();
        this.is_transitioning = true;
        this.checkScrollbar();
        var count = incrementModalOpenCount();

        if (count === 1) {
          this.setScrollbar();
        }

        this.adjustDialog();
        this.setModalOpenClass(true);
        this.setResizeEvent(true);
      },
      onEnter: function onEnter() {
        this.is_block = true;
      },
      onAfterEnter: function onAfterEnter() {
        var _this2 = this;

        this.is_show = true;
        this.is_transitioning = false;
        this.$nextTick(function () {
          var shownEvt = new BvEvent('shown', {
            cancelable: false,
            vueTarget: _this2,
            target: _this2.$refs.modal,
            modalId: _this2.safeId(),
            relatedTarget: null
          });

          _this2.emitEvent(shownEvt);

          _this2.focusFirst();

          _this2.setEnforceFocus(true);
        });
      },
      onBeforeLeave: function onBeforeLeave() {
        this.is_transitioning = true;
        this.setResizeEvent(false);
      },
      onLeave: function onLeave() {
        // Remove the 'show' class
        this.is_show = false;
      },
      onAfterLeave: function onAfterLeave() {
        var _this3 = this;

        this.is_block = false;
        this.resetDialogAdjustments();
        this.is_transitioning = false;
        var count = decrementModalOpenCount();

        if (count === 0) {
          this.resetScrollbar();
          this.setModalOpenClass(false);
        }

        this.setEnforceFocus(false);
        this.$nextTick(function () {
          _this3.is_hidden = _this3.lazy || false;
          _this3.zIndex = ZINDEX_OFFSET;

          _this3.returnFocusTo();

          _this3.is_closing = false;
          var hiddenEvt = new BvEvent('hidden', {
            cancelable: false,
            vueTarget: _this3,
            target: _this3.lazy ? null : _this3.$refs.modal,
            modalId: _this3.safeId(),
            relatedTarget: null
          });

          _this3.emitEvent(hiddenEvt);
        });
      },
      // Event emitter
      emitEvent: function emitEvent(bvEvt) {
        var type = bvEvt.type;
        this.$emit(type, bvEvt);
        this.$root.$emit("bv::modal::".concat(type), bvEvt, this.safeId());
      },
      // UI Event Handlers
      onClickOut: function onClickOut(evt) {
        // Do nothing if not visible, backdrop click disabled, or element that generated
        // click event is no longer in document
        if (!this.is_visible || this.noCloseOnBackdrop || !contains(document, evt.target)) {
          return;
        } // If backdrop clicked, hide modal


        if (!contains(this.$refs.content, evt.target)) {
          this.hide('backdrop');
        }
      },
      onEsc: function onEsc(evt) {
        // If ESC pressed, hide modal
        if (evt.keyCode === KeyCodes.ESC && this.is_visible && !this.noCloseOnEsc) {
          this.hide('esc');
        }
      },
      // Document focusin listener
      focusHandler: function focusHandler(evt) {
        // If focus leaves modal, bring it back
        var modal = this.$refs.modal;

        if (!this.noEnforceFocus && this.isTop && this.is_visible && modal && document !== evt.target && !contains(modal, evt.target)) {
          modal.focus({
            preventScroll: true
          });
        }
      },
      // Turn on/off focusin listener
      setEnforceFocus: function setEnforceFocus(on) {
        var options = {
          passive: true,
          capture: false
        };

        if (on) {
          eventOn(document, 'focusin', this.focusHandler, options);
        } else {
          eventOff(document, 'focusin', this.focusHandler, options);
        }
      },
      // Resize Listener
      setResizeEvent: function setResizeEvent(on)
      /* istanbul ignore next: can't easily test in JSDOM */
      {
        var _this4 = this;
        ['resize', 'orientationchange'].forEach(function (evtName) {
          var options = {
            passive: true,
            capture: false
          };

          if (on) {
            eventOn(window, evtName, _this4.adjustDialog, options);
          } else {
            eventOff(window, evtName, _this4.adjustDialog, options);
          }
        });
      },
      // Root Listener handlers
      showHandler: function showHandler(id, triggerEl) {
        if (id === this.id) {
          this.return_focus = triggerEl || null;
          this.show();
        }
      },
      hideHandler: function hideHandler(id) {
        if (id === this.id) {
          this.hide();
        }
      },
      shownHandler: function shownHandler() {
        this.setTop();
      },
      hiddenHandler: function hiddenHandler() {
        this.setTop();
      },
      setTop: function setTop() {
        // Determine if we are the topmost visible modal
        this.isTop = this.zIndex >= getModalMaxZIndex();
      },
      modalListener: function modalListener(bvEvt) {
        // If another modal opens, close this one
        if (this.noStacking && bvEvt.vueTarget !== this) {
          this.hide();
        }
      },
      // Focus control handlers
      focusFirst: function focusFirst() {
        // Don't try and focus if we are SSR
        if (typeof document === 'undefined') {
          return;
        }

        var modal = this.$refs.modal;
        var activeElement = document.activeElement;

        if (activeElement && contains(modal, activeElement)) {
          // If activeElement is child of modal or is modal, no need to change focus
          return;
        }

        if (modal) {
          // make sure top of modal is showing (if longer than the viewport) and
          // focus the modal content wrapper
          this.$nextTick(function () {
            modal.scrollTop = 0;
            modal.focus();
          });
        }
      },
      returnFocusTo: function returnFocusTo() {
        // Prefer returnFocus prop over event specified return_focus value
        var el = this.returnFocus || this.return_focus || null;

        if (typeof el === 'string') {
          // CSS Selector
          el = select(el);
        }

        if (el) {
          el = el.$el || el;

          if (isVisible(el)) {
            el.focus();
          }
        }
      },
      // Utility methods
      getScrollbarWidth: function getScrollbarWidth() {
        var scrollDiv = document.createElement('div');
        scrollDiv.className = 'modal-scrollbar-measure';
        document.body.appendChild(scrollDiv);
        this.scrollbarWidth = getBCR(scrollDiv).width - scrollDiv.clientWidth;
        document.body.removeChild(scrollDiv);
      },
      setModalOpenClass: function setModalOpenClass(open) {
        if (open) {
          addClass(document.body, 'modal-open');
        } else {
          removeClass(document.body, 'modal-open');
        }
      },
      adjustDialog: function adjustDialog() {
        if (!this.is_visible) {
          return;
        }

        var modal = this.$refs.modal;
        var isModalOverflowing = modal.scrollHeight > document.documentElement.clientHeight;

        if (!this.isBodyOverflowing && isModalOverflowing) {
          modal.style.paddingLeft = "".concat(this.scrollbarWidth, "px");
        } else {
          modal.style.paddingLeft = '';
        }

        if (this.isBodyOverflowing && !isModalOverflowing) {
          modal.style.paddingRight = "".concat(this.scrollbarWidth, "px");
        } else {
          modal.style.paddingRight = '';
        }
      },
      resetDialogAdjustments: function resetDialogAdjustments() {
        var modal = this.$refs.modal;

        if (modal) {
          modal.style.paddingLeft = '';
          modal.style.paddingRight = '';
        }
      },
      checkScrollbar: function checkScrollbar()
      /* istanbul ignore next: getBCR can't be tested in JSDOM */
      {
        var _getBCR = getBCR(document.body),
            left = _getBCR.left,
            right = _getBCR.right,
            height = _getBCR.height; // Extra check for body.height needed for stacked modals


        this.isBodyOverflowing = left + right < window.innerWidth || height > window.innerHeight;
      },
      setScrollbar: function setScrollbar() {
        /* istanbul ignore if: get Computed Style can't be tested in JSDOM */
        if (this.isBodyOverflowing) {
          // Note: DOMNode.style.paddingRight returns the actual value or '' if not set
          //   while $(DOMNode).css('padding-right') returns the calculated value or 0 if not set
          var body = document.body;
          var scrollbarWidth = this.scrollbarWidth;
          body._paddingChangedForModal = [];
          body._marginChangedForModal = []; // Adjust fixed content padding

          selectAll(Selector$1.FIXED_CONTENT).forEach(function (el) {
            var actualPadding = el.style.paddingRight;
            var calculatedPadding = getCS(el).paddingRight || 0;
            setAttr(el, 'data-padding-right', actualPadding);
            el.style.paddingRight = "".concat(parseFloat(calculatedPadding) + scrollbarWidth, "px");

            body._paddingChangedForModal.push(el);
          }); // Adjust sticky content margin

          selectAll(Selector$1.STICKY_CONTENT).forEach(function (el) {
            var actualMargin = el.style.marginRight;
            var calculatedMargin = getCS(el).marginRight || 0;
            setAttr(el, 'data-margin-right', actualMargin);
            el.style.marginRight = "".concat(parseFloat(calculatedMargin) - scrollbarWidth, "px");

            body._marginChangedForModal.push(el);
          }); // Adjust navbar-toggler margin

          selectAll(Selector$1.NAVBAR_TOGGLER).forEach(function (el) {
            var actualMargin = el.style.marginRight;
            var calculatedMargin = getCS(el).marginRight || 0;
            setAttr(el, 'data-margin-right', actualMargin);
            el.style.marginRight = "".concat(parseFloat(calculatedMargin) + scrollbarWidth, "px");

            body._marginChangedForModal.push(el);
          }); // Adjust body padding

          var actualPadding = body.style.paddingRight;
          var calculatedPadding = getCS(body).paddingRight;
          setAttr(body, 'data-padding-right', actualPadding);
          body.style.paddingRight = "".concat(parseFloat(calculatedPadding) + scrollbarWidth, "px");
        }
      },
      resetScrollbar: function resetScrollbar() {
        var body = document.body;

        if (body._paddingChangedForModal) {
          // Restore fixed content padding
          body._paddingChangedForModal.forEach(function (el) {
            if (hasAttr(el, 'data-padding-right')) {
              el.style.paddingRight = getAttr(el, 'data-padding-right') || '';
              removeAttr(el, 'data-padding-right');
            }
          });
        }

        if (body._marginChangedForModal) {
          // Restore sticky content and navbar-toggler margin
          body._marginChangedForModal.forEach(function (el) {
            if (hasAttr(el, 'data-margin-right')) {
              el.style.marginRight = getAttr(el, 'data-margin-right') || '';
              removeAttr(el, 'data-margin-right');
            }
          });
        }

        body._paddingChangedForModal = null;
        body._marginChangedForModal = null; // Restore body padding

        if (hasAttr(body, 'data-padding-right')) {
          body.style.paddingRight = getAttr(body, 'data-padding-right') || '';
          removeAttr(body, 'data-padding-right');
        }
      }
    },
    render: function render(h) {
      var _this5 = this;

      var $slots = this.$slots; // Modal Header

      var header = h(false);

      if (!this.hideHeader) {
        var modalHeader = $slots['modal-header'];

        if (!modalHeader) {
          var closeButton = h(false);

          if (!this.hideHeaderClose) {
            closeButton = h('b-button-close', {
              props: {
                disabled: this.is_transitioning,
                ariaLabel: this.headerCloseLabel,
                textVariant: this.headerTextVariant
              },
              on: {
                click: function click(evt) {
                  _this5.hide('headerclose');
                }
              }
            }, [$slots['modal-header-close']]);
          }

          modalHeader = [h(this.titleTag, {
            class: ['modal-title']
          }, [$slots['modal-title'] || this.titleHtml || stripTags(this.title)]), closeButton];
        }

        header = h('header', {
          ref: 'header',
          staticClass: 'modal-header',
          class: this.headerClasses,
          attrs: {
            id: this.safeId('__BV_modal_header_')
          }
        }, [modalHeader]);
      } // Modal Body


      var body = h('div', {
        ref: 'body',
        staticClass: 'modal-body',
        class: this.bodyClasses,
        attrs: {
          id: this.safeId('__BV_modal_body_')
        }
      }, [$slots.default]); // Modal Footer

      var footer = h(false);

      if (!this.hideFooter) {
        var modalFooter = $slots['modal-footer'];

        if (!modalFooter) {
          var cancelButton = h(false);

          if (!this.okOnly) {
            cancelButton = h('b-button', {
              props: {
                variant: this.cancelVariant,
                size: this.buttonSize,
                disabled: this.cancelDisabled || this.busy || this.is_transitioning
              },
              on: {
                click: function click(evt) {
                  _this5.hide('cancel');
                }
              }
            }, [$slots['modal-cancel'] || this.cancelTitleHtml || stripTags(this.cancelTitle)]);
          }

          var okButton = h('b-button', {
            props: {
              variant: this.okVariant,
              size: this.buttonSize,
              disabled: this.okDisabled || this.busy || this.is_transitioning
            },
            on: {
              click: function click(evt) {
                _this5.hide('ok');
              }
            }
          }, [$slots['modal-ok'] || this.okTitleHtml || stripTags(this.okTitle)]);
          modalFooter = [cancelButton, okButton];
        }

        footer = h('footer', {
          ref: 'footer',
          staticClass: 'modal-footer',
          class: this.footerClasses,
          attrs: {
            id: this.safeId('__BV_modal_footer_')
          }
        }, [modalFooter]);
      } // Assemble Modal Content


      var modalContent = h('div', {
        ref: 'content',
        class: this.contentClasses,
        attrs: {
          role: 'document',
          id: this.safeId('__BV_modal_content_'),
          'aria-labelledby': this.hideHeader ? null : this.safeId('__BV_modal_header_'),
          'aria-describedby': this.safeId('__BV_modal_body_')
        }
      }, [header, body, footer]); // Modal Dialog wrapper

      var modalDialog = h('div', {
        staticClass: 'modal-dialog',
        class: this.dialogClasses
      }, [modalContent]); // Modal

      var modal = h('div', {
        ref: 'modal',
        staticClass: 'modal',
        class: this.modalClasses,
        directives: [{
          name: 'show',
          rawName: 'v-show',
          value: this.is_visible,
          expression: 'is_visible'
        }],
        attrs: {
          id: this.safeId(),
          role: 'dialog',
          tabindex: '-1',
          'aria-hidden': this.is_visible ? null : 'true',
          'aria-modal': this.is_visible ? 'true' : null
        },
        on: {
          keydown: this.onEsc,
          click: this.onClickOut
        }
      }, [modalDialog]); // Wrap modal in transition

      modal = h('transition', {
        props: {
          enterClass: '',
          enterToClass: '',
          enterActiveClass: '',
          leaveClass: '',
          leaveActiveClass: '',
          leaveToClass: ''
        },
        on: {
          'before-enter': this.onBeforeEnter,
          enter: this.onEnter,
          'after-enter': this.onAfterEnter,
          'before-leave': this.onBeforeLeave,
          leave: this.onLeave,
          'after-leave': this.onAfterLeave
        }
      }, [modal]); // Modal Backdrop

      var backdrop = h(false);

      if (!this.hideBackdrop && (this.is_visible || this.is_transitioning)) {
        backdrop = h('div', {
          staticClass: 'modal-backdrop',
          class: this.backdropClasses,
          attrs: {
            id: this.safeId('__BV_modal_backdrop_')
          }
        });
      } // Tab trap to prevent page from scrolling to next element in tab index during enforce focus tab cycle


      var tabTrap = h(false);

      if (this.is_visible && this.isTop && !this.noEnforceFocus) {
        tabTrap = h('div', {
          attrs: {
            tabindex: '0'
          }
        });
      } // Assemble modal and backdrop in an outer div needed for lazy modals


      var outer = h(false);

      if (!this.is_hidden) {
        outer = h('div', {
          key: 'modal-outer',
          style: this.modalOuterStyle,
          attrs: {
            id: this.safeId('__BV_modal_outer_')
          }
        }, [modal, tabTrap, backdrop]);
      } // Wrap in DIV to maintain thi.$el reference for hide/show method aceess


      return h('div', {}, [outer]);
    }
  };

  var listenTypes$1 = {
    click: true
  };
  var bModal = {
    // eslint-disable-next-line no-shadow-restricted-names
    bind: function bind(el, binding, vnode) {
      bindTargets(vnode, binding, listenTypes$1, function (_ref) {
        var targets = _ref.targets,
            vnode = _ref.vnode;
        targets.forEach(function (target) {
          vnode.context.$root.$emit('bv::show::modal', target, vnode.elm);
        });
      });

      if (el.tagName !== 'BUTTON') {
        // If element is not a button, we add `role="button"` for accessibility
        setAttr(el, 'role', 'button');
      }
    },
    unbind: function unbind(el, binding, vnode) {
      unbindTargets(vnode, binding, listenTypes$1);

      if (el.tagName !== 'BUTTON') {
        // If element is not a button, we add `role="button"` for accessibility
        removeAttr(el, 'role', 'button');
      }
    }
  };

  var directives$1 = {
    bModal: bModal
  };
  var modalDirectivePlugin = {
    install: function install(Vue) {
      registerDirectives(Vue, directives$1);
    }
  };

  var components$q = {
    BModal: BModal
  };
  var index$o = {
    install: function install(Vue) {
      registerComponents(Vue, components$q);
      Vue.use(modalDirectivePlugin);
    }
  };

  var props$B = {
    tag: {
      type: String,
      default: 'ul'
    },
    fill: {
      type: Boolean,
      default: false
    },
    justified: {
      type: Boolean,
      default: false
    },
    tabs: {
      type: Boolean,
      default: false
    },
    pills: {
      type: Boolean,
      default: false
    },
    vertical: {
      type: Boolean,
      default: false
    },
    isNavBar: {
      type: Boolean,
      default: false
    } // @vue/component

  };
  var BNav = {
    name: 'BNav',
    functional: true,
    props: props$B,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;

      if (props.isNavBar) {
        warn("b-nav: Prop 'is-nav-bar' is deprecated. Please use component '<b-navbar-nav>' instead.");
      }

      return h(props.tag, mergeData(data, {
        class: {
          nav: !props.isNavBar,
          'navbar-nav': props.isNavBar,
          'nav-tabs': props.tabs && !props.isNavBar,
          'nav-pills': props.pills && !props.isNavBar,
          'flex-column': props.vertical && !props.isNavBar,
          'nav-fill': props.fill,
          'nav-justified': props.justified
        }
      }), children);
    }
  };

  var props$C = propsFactory(); // @vue/component

  var BNavItem = {
    name: 'BNavItem',
    functional: true,
    props: props$C,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h('li', mergeData(data, {
        staticClass: 'nav-item'
      }), [h(BLink, {
        staticClass: 'nav-link',
        props: props
      }, children)]);
    }
  };

  var props$D = {
    tag: {
      type: String,
      default: 'span'
    } // @vue/component

  };
  var BNavText = {
    name: 'BNavText',
    functional: true,
    props: props$D,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        staticClass: 'navbar-text'
      }), children);
    }
  };

  var BNavForm = {
    name: 'BNavForm',
    functional: true,
    props: {
      id: {
        type: String,
        default: null
      }
    },
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(BForm, mergeData(data, {
        attrs: {
          id: props.id
        },
        props: {
          inline: true
        }
      }), children);
    }
  };

  var BNavItemDropdown = {
    name: 'BNavItemDropdown',
    mixins: [idMixin, dropdownMixin],
    props: {
      noCaret: {
        type: Boolean,
        default: false
      },
      extraToggleClasses: {
        // Extra Toggle classes
        type: String,
        default: ''
      },
      extraMenuClasses: {
        // Extra Menu classes
        type: String,
        default: ''
      },
      role: {
        type: String,
        default: 'menu'
      }
    },
    computed: {
      isNav: function isNav() {
        // Signal to dropdown mixin that we are in a navbar
        return true;
      },
      dropdownClasses: function dropdownClasses() {
        return ['nav-item', 'b-nav-dropdown', 'dropdown', this.dropup ? 'dropup' : '', this.visible ? 'show' : ''];
      },
      toggleClasses: function toggleClasses() {
        return ['nav-link', this.noCaret ? '' : 'dropdown-toggle', this.disabled ? 'disabled' : '', this.extraToggleClasses ? this.extraToggleClasses : ''];
      },
      menuClasses: function menuClasses() {
        return ['dropdown-menu', this.right ? 'dropdown-menu-right' : 'dropdown-menu-left', this.visible ? 'show' : '', this.extraMenuClasses ? this.extraMenuClasses : ''];
      }
    },
    render: function render(h) {
      var button = h('a', {
        class: this.toggleClasses,
        ref: 'toggle',
        attrs: {
          href: '#',
          id: this.safeId('_BV_button_'),
          disabled: this.disabled,
          'aria-haspopup': 'true',
          'aria-expanded': this.visible ? 'true' : 'false'
        },
        on: {
          click: this.toggle,
          keydown: this.toggle // space, enter, down

        }
      }, [this.$slots['button-content'] || this.$slots.text || h('span', {
        domProps: htmlOrText(this.html, this.text)
      })]);
      var menu = h('div', {
        class: this.menuClasses,
        ref: 'menu',
        attrs: {
          tabindex: '-1',
          'aria-labelledby': this.safeId('_BV_button_')
        },
        on: {
          mouseover: this.onMouseOver,
          keydown: this.onKeydown // tab, up, down, esc

        }
      }, [this.$slots.default]);
      return h('li', {
        attrs: {
          id: this.safeId()
        },
        class: this.dropdownClasses
      }, [button, menu]);
    }
  };

  var components$r = {
    BNav: BNav,
    BNavItem: BNavItem,
    BNavText: BNavText,
    BNavForm: BNavForm,
    BNavItemDropdown: BNavItemDropdown,
    BNavItemDd: BNavItemDropdown,
    BNavDropdown: BNavItemDropdown,
    BNavDd: BNavItemDropdown
  };
  var navPlugin = {
    install: function install(Vue) {
      registerComponents(Vue, components$r);
      Vue.use(dropdownPlugin);
    }
  };

  var props$E = {
    tag: {
      type: String,
      default: 'nav'
    },
    type: {
      type: String,
      default: 'light'
    },
    variant: {
      type: String
    },
    toggleable: {
      type: [Boolean, String],
      default: false
    },
    fixed: {
      type: String
    },
    sticky: {
      type: Boolean,
      default: false
    },
    print: {
      type: Boolean,
      default: false
    } // @vue/component

  };
  var BNavbar = {
    name: 'BNavbar',
    functional: true,
    props: props$E,
    render: function render(h, _ref) {
      var _class;

      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var breakpoint = '';

      if (props.toggleable && typeof props.toggleable === 'string' && props.toggleable !== 'xs') {
        breakpoint = "navbar-expand-".concat(props.toggleable);
      } else if (props.toggleable === false) {
        breakpoint = 'navbar-expand';
      }

      return h(props.tag, mergeData(data, {
        staticClass: 'navbar',
        class: (_class = {
          'd-print': props.print,
          'sticky-top': props.sticky
        }, _defineProperty(_class, "navbar-".concat(props.type), Boolean(props.type)), _defineProperty(_class, "bg-".concat(props.variant), Boolean(props.variant)), _defineProperty(_class, "fixed-".concat(props.fixed), Boolean(props.fixed)), _defineProperty(_class, "".concat(breakpoint), Boolean(breakpoint)), _class),
        attrs: {
          role: props.tag === 'nav' ? null : 'navigation'
        }
      }), children);
    }
  };

  var props$F = {
    tag: {
      type: String,
      default: 'ul'
    },
    fill: {
      type: Boolean,
      default: false
    },
    justified: {
      type: Boolean,
      default: false
    } // @vue/component

  };
  var BNavbarNav = {
    name: 'BNavbarNav',
    functional: true,
    props: props$F,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      return h(props.tag, mergeData(data, {
        staticClass: 'navbar-nav',
        class: {
          'nav-fill': props.fill,
          'nav-justified': props.justified
        }
      }), children);
    }
  };

  var linkProps$3 = propsFactory();
  linkProps$3.href.default = undefined;
  linkProps$3.to.default = undefined;
  var props$G = _objectSpread({}, linkProps$3, {
    tag: {
      type: String,
      default: 'div'
    } // @vue/component

  });
  var BNavbarBrand = {
    name: 'BNavbarBrand',
    functional: true,
    props: props$G,
    render: function render(h, _ref) {
      var props = _ref.props,
          data = _ref.data,
          children = _ref.children;
      var isLink = Boolean(props.to || props.href);
      var tag = isLink ? BLink : props.tag;
      return h(tag, mergeData(data, {
        staticClass: 'navbar-brand',
        props: isLink ? pluckProps(linkProps$3, props) : {}
      }), children);
    }
  };

  var BNavbarToggle = {
    name: 'BNavbarToggle',
    mixins: [listenOnRootMixin],
    props: {
      label: {
        type: String,
        default: 'Toggle navigation'
      },
      target: {
        type: String,
        required: true
      }
    },
    data: function data() {
      return {
        toggleState: false
      };
    },
    created: function created() {
      this.listenOnRoot('bv::collapse::state', this.handleStateEvt);
    },
    methods: {
      onClick: function onClick(evt) {
        this.$emit('click', evt);
        /* istanbul ignore next */

        if (!evt.defaultPrevented) {
          this.$root.$emit('bv::toggle::collapse', this.target);
        }
      },
      handleStateEvt: function handleStateEvt(id, state) {
        if (id === this.target) {
          this.toggleState = state;
        }
      }
    },
    render: function render(h) {
      return h('button', {
        class: ['navbar-toggler'],
        attrs: {
          type: 'button',
          'aria-label': this.label,
          'aria-controls': this.target,
          'aria-expanded': this.toggleState ? 'true' : 'false'
        },
        on: {
          click: this.onClick
        }
      }, [this.$slots.default || h('span', {
        class: ['navbar-toggler-icon']
      })]);
    }
  };

  var components$s = {
    BNavbar: BNavbar,
    BNavbarNav: BNavbarNav,
    BNavbarBrand: BNavbarBrand,
    BNavbarToggle: BNavbarToggle,
    BNavToggle: BNavbarToggle
  };
  var index$p = {
    install: function install(Vue) {
      registerComponents(Vue, components$s);
      Vue.use(navPlugin);
      Vue.use(collapsePlugin);
      Vue.use(dropdownPlugin);
    }
  };

  /**
   * @param {number} length
   * @return {Array}
   */
  var range = (function (length) {
    return Array.apply(null, {
      length: length
    });
  });

  /*
   * Comon props, computed, data, render function, and methods for b-pagination and b-pagination-nav
   */

  var ELLIPSIS_THRESHOLD = 3; // Default # of buttons limit

  var DEFAULT_LIMIT = 5; // Make an array of N to N+X

  function makePageArray(startNum, numPages) {
    return range(numPages).map(function (value, index) {
      return {
        number: index + startNum,
        classes: null
      };
    });
  } // Sanitize the provided Limit value (converting to a number)


  function sanitizeLimit(value) {
    var limit = parseInt(value, 10) || 1;
    return limit < 1 ? DEFAULT_LIMIT : limit;
  } // Sanitize the provided numberOfPages value (converting to a number)


  function sanitizeNumPages(value) {
    var num = parseInt(value, 10) || 1;
    return num < 1 ? 1 : num;
  } // Sanitize the provided current page number (converting to a number)


  function sanitizeCurPage(value, numPages) {
    var page = parseInt(value, 10) || 1;
    return page > numPages ? numPages : page < 1 ? 1 : page;
  } // Links don't normally respond to SPACE, so we add that functionality via this handler


  function onSpaceKey(evt) {
    if (evt.keyCode === KeyCodes.SPACE) {
      evt.preventDefault(); // Stop page from scrolling

      evt.stopImmediatePropagation();
      evt.stopPropagation(); // Trigger the click event on the link

      evt.currentTarget.click();
      return false;
    }
  } // Props object


  var props$H = {
    disabled: {
      type: Boolean,
      default: false
    },
    value: {
      type: [Number, String],
      default: 1,
      validator: function validator(value) {
        var num = parseInt(value, 10);
        /* istanbul ignore if */

        if (isNaN(num) || num < 1) {
          warn('pagination: v-model value must be a number greater than 0');
          return false;
        }

        return true;
      }
    },
    limit: {
      type: [Number, String],
      default: DEFAULT_LIMIT,
      validator: function validator(value) {
        var num = parseInt(value, 10);
        /* istanbul ignore if */

        if (isNaN(num) || num < 1) {
          warn('pagination: prop "limit" must be a number greater than 0');
          return false;
        }

        return true;
      }
    },
    size: {
      type: String,
      default: 'md'
    },
    align: {
      type: String,
      default: 'left'
    },
    hideGotoEndButtons: {
      type: Boolean,
      default: false
    },
    ariaLabel: {
      type: String,
      default: 'Pagination'
    },
    labelFirstPage: {
      type: String,
      default: 'Go to first page'
    },
    firstText: {
      type: String,
      default: '«'
    },
    labelPrevPage: {
      type: String,
      default: 'Go to previous page'
    },
    prevText: {
      type: String,
      default: '‹'
    },
    labelNextPage: {
      type: String,
      default: 'Go to next page'
    },
    nextText: {
      type: String,
      default: '›'
    },
    labelLastPage: {
      type: String,
      default: 'Go to last page'
    },
    lastText: {
      type: String,
      default: '»'
    },
    labelPage: {
      type: String,
      default: 'Go to page'
    },
    hideEllipsis: {
      type: Boolean,
      default: false
    },
    ellipsisText: {
      type: String,
      default: '…'
    } // @vue/component

  };
  var paginationMixin = {
    components: {
      BLink: BLink
    },
    props: props$H,
    data: function data() {
      return {
        currentPage: 1,
        localNumPages: 1,
        localLimit: DEFAULT_LIMIT
      };
    },
    computed: {
      btnSize: function btnSize() {
        return this.size ? "pagination-".concat(this.size) : '';
      },
      alignment: function alignment() {
        if (this.align === 'center') {
          return 'justify-content-center';
        } else if (this.align === 'end' || this.align === 'right') {
          return 'justify-content-end';
        }

        return '';
      },
      paginationParams: function paginationParams() {
        // Determine if we should show the the ellipsis
        var limit = this.limit;
        var numPages = this.localNumPages;
        var curPage = this.currentPage;
        var hideEllipsis = this.hideEllipsis;
        var showFirstDots = false;
        var showLastDots = false;
        var numLinks = limit;
        var startNum = 1;

        if (numPages <= limit) {
          // Special Case: Less pages available than the limit of displayed pages
          numLinks = numPages;
        } else if (curPage < limit - 1 && limit > ELLIPSIS_THRESHOLD) {
          // We are near the beginning of the page list
          if (!hideEllipsis) {
            showLastDots = true;
            numLinks = limit - 1;
          }
        } else if (numPages - curPage + 2 < limit && limit > ELLIPSIS_THRESHOLD) {
          // We are near the end of the list
          if (!hideEllipsis) {
            numLinks = limit - 1;
            showFirstDots = true;
          }

          startNum = numPages - numLinks + 1;
        } else {
          // We are somewhere in the middle of the page list
          if (limit > ELLIPSIS_THRESHOLD && !hideEllipsis) {
            numLinks = limit - 2;
            showFirstDots = showLastDots = true;
          }

          startNum = curPage - Math.floor(numLinks / 2);
        } // Sanity checks


        if (startNum < 1) {
          startNum = 1;
        } else if (startNum > numPages - numLinks) {
          startNum = numPages - numLinks + 1;
        }

        return {
          showFirstDots: showFirstDots,
          showLastDots: showLastDots,
          numLinks: numLinks,
          startNum: startNum
        };
      },
      pageList: function pageList() {
        // Generates the pageList array
        var _this$paginationParam = this.paginationParams,
            numLinks = _this$paginationParam.numLinks,
            startNum = _this$paginationParam.startNum; // Generate list of page numbers

        var pages = makePageArray(startNum, numLinks); // We limit to a total of 3 page buttons on XS screens
        // So add classes to page links to hide them for XS breakpoint
        // Note: Ellipsis will also be hidden on XS screens
        // TODO: Make this visual limit configurable based on breakpoint(s)

        if (pages.length > 3) {
          var idx = this.currentPage - startNum;

          if (idx === 0) {
            // Keep leftmost 3 buttons visible when current page is first page
            for (var i = 3; i < pages.length; i++) {
              pages[i].classes = 'd-none d-sm-flex';
            }
          } else if (idx === pages.length - 1) {
            // Keep rightmost 3 buttons visible when current page is last page
            for (var _i = 0; _i < pages.length - 3; _i++) {
              pages[_i].classes = 'd-none d-sm-flex';
            }
          } else {
            // Hide all except current page, current page - 1 and current page + 1
            for (var _i2 = 0; _i2 < idx - 1; _i2++) {
              // hide some left button(s)
              pages[_i2].classes = 'd-none d-sm-flex';
            }

            for (var _i3 = pages.length - 1; _i3 > idx + 1; _i3--) {
              // hide some right button(s)
              pages[_i3].classes = 'd-none d-sm-flex';
            }
          }
        }

        return pages;
      }
    },
    watch: {
      value: function value(newValue, oldValue) {
        if (newValue !== oldValue) {
          this.currentPage = sanitizeCurPage(newValue, this.localNumPages);
        }
      },
      currentPage: function currentPage(newValue, oldValue) {
        if (newValue !== oldValue) {
          this.$emit('input', newValue);
        }
      },
      numberOfPages: function numberOfPages(newValue, oldValue) {
        if (newValue !== oldValue) {
          this.localNumPages = sanitizeNumPages(newValue);
        }
      },
      limit: function limit(newValue, oldValue) {
        if (newValue !== oldValue) {
          this.localLimit = sanitizeLimit(newValue);
        }
      }
    },
    created: function created() {
      // Set our default values in data
      this.localLimit = sanitizeLimit(this.limit);
      this.localNumPages = sanitizeNumPages(this.numberOfPages);
      this.currentPage = sanitizeCurPage(this.value, this.localNumPages);
    },
    methods: {
      getButtons: function getButtons() {
        // Return only buttons that are visible
        return selectAll('a.page-link', this.$el).filter(function (btn) {
          return isVisible(btn);
        });
      },
      setBtnFocus: function setBtnFocus(btn) {
        btn.focus();
      },
      focusCurrent: function focusCurrent() {
        var _this = this;

        // We do this in next tick to ensure buttons have finished rendering
        this.$nextTick(function () {
          var btn = _this.getButtons().find(function (el) {
            return parseInt(getAttr(el, 'aria-posinset'), 10) === _this.currentPage;
          });

          if (btn && btn.focus) {
            _this.setBtnFocus(btn);
          } else {
            // Fallback if current page is not in button list
            _this.focusFirst();
          }
        });
      },
      focusFirst: function focusFirst() {
        var _this2 = this;

        // We do this in next tick to ensure buttons have finished rendering
        this.$nextTick(function () {
          var btn = _this2.getButtons().find(function (el) {
            return !isDisabled(el);
          });

          if (btn && btn.focus && btn !== document.activeElement) {
            _this2.setBtnFocus(btn);
          }
        });
      },
      focusLast: function focusLast() {
        var _this3 = this;

        // We do this in next tick to ensure buttons have finished rendering
        this.$nextTick(function () {
          var btn = _this3.getButtons().reverse().find(function (el) {
            return !isDisabled(el);
          });

          if (btn && btn.focus && btn !== document.activeElement) {
            _this3.setBtnFocus(btn);
          }
        });
      },
      focusPrev: function focusPrev() {
        var _this4 = this;

        // We do this in next tick to ensure buttons have finished rendering
        this.$nextTick(function () {
          var buttons = _this4.getButtons();

          var idx = buttons.indexOf(document.activeElement);

          if (idx > 0 && !isDisabled(buttons[idx - 1]) && buttons[idx - 1].focus) {
            _this4.setBtnFocus(buttons[idx - 1]);
          }
        });
      },
      focusNext: function focusNext() {
        var _this5 = this;

        // We do this in next tick to ensure buttons have finished rendering
        this.$nextTick(function () {
          var buttons = _this5.getButtons();

          var idx = buttons.indexOf(document.activeElement);
          var cnt = buttons.length - 1;

          if (idx < cnt && !isDisabled(buttons[idx + 1]) && buttons[idx + 1].focus) {
            _this5.setBtnFocus(buttons[idx + 1]);
          }
        });
      }
    },
    render: function render(h) {
      var _this6 = this;

      var buttons = [];
      var numberOfPages = this.localNumPages;
      var disabled = this.disabled;
      var _this$paginationParam2 = this.paginationParams,
          showFirstDots = _this$paginationParam2.showFirstDots,
          showLastDots = _this$paginationParam2.showLastDots; // Helper function

      var isActivePage = function isActivePage(pageNum) {
        return pageNum === _this6.currentPage;
      }; // Factory function for prev/next/first/last buttons


      var makeEndBtn = function makeEndBtn(linkTo, ariaLabel, btnSlot, btnText, pageTest, key) {
        var button;
        var domProps = btnSlot ? {} : {
          textContent: btnText
        };
        var staticClass = 'page-item';
        var attrs = {
          role: 'none presentation',
          'aria-hidden': disabled ? 'true' : null
        };

        if (disabled || isActivePage(pageTest) || linkTo < 1 || linkTo > numberOfPages) {
          button = h('li', {
            key: key,
            attrs: attrs,
            staticClass: staticClass,
            class: ['disabled']
          }, [h('span', {
            staticClass: 'page-link',
            domProps: domProps
          }, [btnSlot])]);
        } else {
          button = h('li', {
            key: key,
            attrs: attrs,
            staticClass: staticClass
          }, [h('b-link', {
            staticClass: 'page-link',
            props: _this6.linkProps(linkTo),
            attrs: {
              role: 'menuitem',
              tabindex: '-1',
              'aria-label': ariaLabel,
              'aria-controls': _this6.ariaControls || null
            },
            on: {
              click: function click(evt) {
                _this6.onClick(linkTo, evt);
              },
              keydown: onSpaceKey
            }
          }, [h('span', {
            domProps: domProps
          }, [btnSlot])])]);
        }

        return button;
      }; // Ellipsis factory


      var makeEllipsis = function makeEllipsis(isLast) {
        return h('li', {
          key: "elipsis-".concat(isLast ? 'last' : 'first'),
          class: ['page-item', 'disabled', 'd-none', 'd-sm-flex'],
          attrs: {
            role: 'separator'
          }
        }, [_this6.$slots['ellipsis-text'] || h('span', {
          class: ['page-link'],
          domProps: {
            textContent: _this6.ellipsisText
          }
        })]);
      }; // Goto First Page button bookend


      buttons.push(this.hideGotoEndButtons ? h(false) : makeEndBtn(1, this.labelFirstPage, this.$slots['first-text'], stripTags(this.firstText), 1, 'bookend-goto-first')); // Goto Previous page button bookend

      buttons.push(makeEndBtn(this.currentPage - 1, this.labelPrevPage, this.$slots['prev-text'], stripTags(this.prevText), 1, 'bookend-goto-prev')); // First Ellipsis Bookend

      buttons.push(showFirstDots ? makeEllipsis(false) : h(false)); // Individual Page links

      this.pageList.forEach(function (page) {
        var inner;

        var pageText = _this6.makePage(page.number);

        var active = isActivePage(page.number);
        var staticClass = 'page-link';
        var attrs = {
          role: 'menuitemradio',
          'aria-disabled': disabled ? 'true' : null,
          'aria-controls': _this6.ariaControls || null,
          'aria-label': "".concat(_this6.labelPage, " ").concat(page.number),
          'aria-checked': active ? 'true' : 'false',
          'aria-posinset': page.number,
          'aria-setsize': numberOfPages,
          // ARIA "roving tabindex" method
          tabindex: disabled ? null : active ? '0' : '-1'
        };

        if (disabled) {
          inner = h('span', {
            key: "page-".concat(page.number, "-link-disabled"),
            staticClass: staticClass,
            attrs: attrs
          }, pageText);
        } else {
          inner = h('b-link', {
            key: "page-".concat(page.number, "-link"),
            props: _this6.linkProps(page.number),
            staticClass: staticClass,
            attrs: attrs,
            on: {
              click: function click(evt) {
                _this6.onClick(page.number, evt);
              },
              keydown: onSpaceKey
            }
          }, pageText);
        }

        buttons.push(h('li', {
          key: "page-".concat(page.number),
          staticClass: 'page-item',
          class: [disabled ? 'disabled' : '', active ? 'active' : '', page.classes],
          attrs: {
            role: 'none presentation'
          }
        }, [inner]));
      }); // Last Ellipsis Bookend

      buttons.push(showLastDots ? makeEllipsis(true) : h(false)); // Goto Next page button bookend

      buttons.push(makeEndBtn(this.currentPage + 1, this.labelNextPage, this.$slots['next-text'], this.nextText, numberOfPages, 'bookend-goto-next')); // Goto Last Page button bookend

      buttons.push(this.hideGotoEndButtons ? h(false) : makeEndBtn(numberOfPages, this.labelLastPage, this.$slots['last-text'], this.lastText, numberOfPages, 'bookend-goto-last')); // Assemble the paginatiom buttons

      var pagination = h('ul', {
        ref: 'ul',
        class: ['pagination', 'b-pagination', this.btnSize, this.alignment],
        attrs: {
          role: 'menubar',
          'aria-disabled': disabled ? 'true' : 'false',
          'aria-label': this.ariaLabel || null
        },
        on: {
          keydown: function keydown(evt) {
            var keyCode = evt.keyCode;
            var shift = evt.shiftKey;

            if (keyCode === KeyCodes.LEFT) {
              evt.preventDefault();
              shift ? _this6.focusFirst() : _this6.focusPrev();
            } else if (keyCode === KeyCodes.RIGHT) {
              evt.preventDefault();
              shift ? _this6.focusLast() : _this6.focusNext();
            }
          }
        }
      }, buttons); // if we are pagination-nav, wrap in '<nav>' wrapper

      if (this.isNav) {
        return h('nav', {
          attrs: {
            'aria-disabled': disabled ? 'true' : null,
            'aria-hidden': disabled ? 'true' : 'false'
          }
        }, [pagination]);
      } else {
        return pagination;
      }
    }
  };

  var DEFAULT_PER_PAGE = 20;
  var DEFAULT_TOTAL_ROWS = 0;

  function sanitizePerPage(value) {
    var perPage = parseInt(value, 10) || DEFAULT_PER_PAGE;
    return perPage < 1 ? 1 : perPage;
  }

  function sanitizeTotalRows(value) {
    var totalRows = parseInt(value, 10) || DEFAULT_TOTAL_ROWS;
    return totalRows < 0 ? 0 : totalRows;
  }

  var props$I = {
    perPage: {
      type: [Number, String],
      default: DEFAULT_PER_PAGE
    },
    totalRows: {
      type: [Number, String],
      default: DEFAULT_TOTAL_ROWS
    },
    ariaControls: {
      type: String,
      default: null
    } // Our render function is brought in from the pagination mixin
    // @vue/component

  };
  var BPagination = {
    name: 'BPagination',
    mixins: [paginationMixin],
    props: props$I,
    computed: {
      numberOfPages: function numberOfPages() {
        var result = Math.ceil(sanitizeTotalRows(this.totalRows) / sanitizePerPage(this.perPage));
        return result < 1 ? 1 : result;
      }
    },
    methods: {
      // These methods are used by the render function
      onClick: function onClick(num, evt) {
        var _this = this;

        // Handle edge cases where number of pages has changed (i.e. if perPage changes)
        if (num > this.numberOfPages) {
          num = this.numberOfPages;
        } else if (num < 1) {
          num = 1;
        } // Update the v-model


        this.currentPage = num; // Emit event triggered by user interaction

        this.$emit('change', this.currentPage);
        this.$nextTick(function () {
          // Keep the current button focused if possible
          var target = evt.target;

          if (isVisible(target) && _this.$el.contains(target) && target.focus) {
            target.focus();
          } else {
            _this.focusCurrent();
          }
        });
      },
      makePage: function makePage(pagenum) {
        return pagenum;
      },
      linkProps: function linkProps(pagenum) {
        // Always '#' for pagination component
        return {
          href: '#'
        };
      }
    }
  };

  var components$t = {
    BPagination: BPagination
  };
  var index$q = {
    install: function install(Vue) {
      registerComponents(Vue, components$t);
    }
  };

  var routerProps = pickLinkProps('activeClass', 'exactActiveClass', 'append', 'exact', 'replace', 'target', 'rel'); // Props object

  var props$J = _objectSpread({
    // pagination-nav specific props
    numberOfPages: {
      type: [Number, String],
      default: 1,
      validator: function validator(value) {
        var num = parseInt(value, 10);
        /* istanbul ignore if */

        if (isNaN(num) || num < 1) {
          warn('b-pagination: prop "number-of-pages" must be a number greater than 0');
          return false;
        }

        return true;
      }
    },
    baseUrl: {
      type: String,
      default: '/'
    },
    useRouter: {
      type: Boolean,
      default: false
    },
    linkGen: {
      type: Function,
      default: null
    },
    pageGen: {
      type: Function,
      default: null
    }
  }, routerProps); // Our render function is brought in via the pagination mixin
  // @vue/component


  var BPaginationNav = {
    name: 'BPaginatonNav',
    mixins: [paginationMixin],
    props: props$J,
    computed: {
      // Used by render function to trigger wraping in '<nav>' element
      isNav: function isNav() {
        return true;
      }
    },
    methods: {
      onClick: function onClick(pageNum, evt) {
        // Update the v-model
        this.currentPage = pageNum;
        this.$nextTick(function () {
          try {
            // Emulate native link click page reloading behaviour by  blurring the
            // paginator and returing focus to the document
            var target = evt.currentTarget || evt.target;
            target.blur();
          } catch (e) {}
        });
      },
      makePage: function makePage(pagenum) {
        if (this.pageGen && typeof this.pageGen === 'function') {
          return this.pageGen(pagenum);
        }

        return pagenum;
      },
      makeLink: function makeLink(pagenum) {
        if (this.linkGen && typeof this.linkGen === 'function') {
          return this.linkGen(pagenum);
        }

        var link = "".concat(this.baseUrl).concat(pagenum);
        return this.useRouter ? {
          path: link
        } : link;
      },
      linkProps: function linkProps(pagenum) {
        var link = this.makeLink(pagenum);
        var props = {
          href: typeof link === 'string' ? link : void 0,
          target: this.target || null,
          rel: this.rel || null,
          disabled: this.disabled
        };

        if (this.useRouter || _typeof(link) === 'object') {
          props = _objectSpread({}, props, {
            to: link,
            exact: this.exact,
            activeClass: this.activeClass,
            exactActiveClass: this.exactActiveClass,
            append: this.append,
            replace: this.replace
          });
        }

        return props;
      }
    }
  };

  var components$u = {
    BPaginationNav: BPaginationNav
  };
  var index$r = {
    install: function install(Vue) {
      registerComponents(Vue, components$u);
    }
  };

  var NAME = 'tooltip';
  var CLASS_PREFIX = 'bs-tooltip';
  var BSCLS_PREFIX_REGEX = new RegExp("\\b".concat(CLASS_PREFIX, "\\S+"), 'g');
  var TRANSITION_DURATION = 150; // Modal $root hidden event

  var MODAL_CLOSE_EVENT = 'bv::modal::hidden'; // Modal container for appending tip/popover

  var MODAL_CLASS = '.modal-content';
  var AttachmentMap$1 = {
    AUTO: 'auto',
    TOP: 'top',
    RIGHT: 'right',
    BOTTOM: 'bottom',
    LEFT: 'left',
    TOPLEFT: 'top',
    TOPRIGHT: 'top',
    RIGHTTOP: 'right',
    RIGHTBOTTOM: 'right',
    BOTTOMLEFT: 'bottom',
    BOTTOMRIGHT: 'bottom',
    LEFTTOP: 'left',
    LEFTBOTTOM: 'left'
  };
  var OffsetMap = {
    AUTO: 0,
    TOPLEFT: -1,
    TOP: 0,
    TOPRIGHT: +1,
    RIGHTTOP: -1,
    RIGHT: 0,
    RIGHTBOTTOM: +1,
    BOTTOMLEFT: -1,
    BOTTOM: 0,
    BOTTOMRIGHT: +1,
    LEFTTOP: -1,
    LEFT: 0,
    LEFTBOTTOM: +1
  };
  var HoverState = {
    SHOW: 'show',
    OUT: 'out'
  };
  var ClassName = {
    FADE: 'fade',
    SHOW: 'show'
  };
  var Selector$2 = {
    TOOLTIP: '.tooltip',
    TOOLTIP_INNER: '.tooltip-inner',
    ARROW: '.arrow' // ESLINT: Not used
    // const Trigger = {
    //   HOVER: 'hover',
    //   FOCUS: 'focus',
    //   CLICK: 'click',
    //   BLUR: 'blur',
    //   MANUAL: 'manual'
    // }

  };
  var Defaults$1 = {
    animation: true,
    template: '<div class="tooltip" role="tooltip">' + '<div class="arrow"></div>' + '<div class="tooltip-inner"></div>' + '</div>',
    trigger: 'hover focus',
    title: '',
    delay: 0,
    html: false,
    placement: 'top',
    offset: 0,
    arrowPadding: 6,
    container: false,
    fallbackPlacement: 'flip',
    callbacks: {},
    boundary: 'scrollParent' // Transition Event names

  };
  var TransitionEndEvents$1 = {
    WebkitTransition: ['webkitTransitionEnd'],
    MozTransition: ['transitionend'],
    OTransition: ['otransitionend', 'oTransitionEnd'],
    transition: ['transitionend'] // Client Side Tip ID counter for aria-describedby attribute
    // Could use Alex's uid generator util
    // Each tooltip requires a unique client side ID

  };
  var NEXTID = 1;
  /* istanbul ignore next */

  function generateId(name) {
    return "__BV_".concat(name, "_").concat(NEXTID++, "__");
  }
  /*
   * ToolTip Class definition
   */

  /* istanbul ignore next: difficult to test in Jest/JSDOM environment */


  var ToolTip =
  /*#__PURE__*/
  function () {
    // Main constructor
    function ToolTip(element, config, $root) {
      _classCallCheck(this, ToolTip);

      // New tooltip object
      this.$isEnabled = true;
      this.$fadeTimeout = null;
      this.$hoverTimeout = null;
      this.$visibleInterval = null;
      this.$hoverState = '';
      this.$activeTrigger = {};
      this.$popper = null;
      this.$element = element;
      this.$tip = null;
      this.$id = generateId(this.constructor.NAME);
      this.$root = $root || null;
      this.$routeWatcher = null; // We use a bound version of the following handlers for root/modal listeners to maintain the 'this' context

      this.$forceHide = this.forceHide.bind(this);
      this.$doHide = this.doHide.bind(this);
      this.$doShow = this.doShow.bind(this);
      this.$doDisable = this.doDisable.bind(this);
      this.$doEnable = this.doEnable.bind(this); // Set the configuration

      this.updateConfig(config);
    } // NOTE: Overridden by PopOver class


    _createClass(ToolTip, [{
      key: "updateConfig",
      // Update config
      value: function updateConfig(config) {
        // Merge config into defaults. We use "this" here because PopOver overrides Default
        var updatedConfig = _objectSpread({}, this.constructor.Default, config); // Sanitize delay


        if (config.delay && typeof config.delay === 'number') {
          updatedConfig.delay = {
            show: config.delay,
            hide: config.delay
          };
        } // Title for tooltip and popover


        if (config.title && typeof config.title === 'number') {
          updatedConfig.title = config.title.toString();
        } // Content only for popover


        if (config.content && typeof config.content === 'number') {
          updatedConfig.content = config.content.toString();
        } // Hide element original title if needed


        this.fixTitle(); // Update the config

        this.$config = updatedConfig; // Stop/Restart listening

        this.unListen();
        this.listen();
      } // Destroy this instance

    }, {
      key: "destroy",
      value: function destroy() {
        // Stop listening to trigger events
        this.unListen(); // Disable while open listeners/watchers

        this.setWhileOpenListeners(false); // Clear any timeouts

        clearTimeout(this.$hoverTimeout);
        this.$hoverTimeout = null;
        clearTimeout(this.$fadeTimeout);
        this.$fadeTimeout = null; // Remove popper

        if (this.$popper) {
          this.$popper.destroy();
        }

        this.$popper = null; // Remove tip from document

        if (this.$tip && this.$tip.parentElement) {
          this.$tip.parentElement.removeChild(this.$tip);
        }

        this.$tip = null; // Null out other properties

        this.$id = null;
        this.$isEnabled = null;
        this.$root = null;
        this.$element = null;
        this.$config = null;
        this.$hoverState = null;
        this.$activeTrigger = null;
        this.$forceHide = null;
        this.$doHide = null;
        this.$doShow = null;
        this.$doDisable = null;
        this.$doEnable = null;
      }
    }, {
      key: "enable",
      value: function enable() {
        // Create a non-cancelable BvEvent
        var enabledEvt = new BvEvent('enabled', {
          cancelable: false,
          target: this.$element,
          relatedTarget: null
        });
        this.$isEnabled = true;
        this.emitEvent(enabledEvt);
      }
    }, {
      key: "disable",
      value: function disable() {
        // Create a non-cancelable BvEvent
        var disabledEvt = new BvEvent('disabled', {
          cancelable: false,
          target: this.$element,
          relatedTarget: null
        });
        this.$isEnabled = false;
        this.emitEvent(disabledEvt);
      } // Click toggler

    }, {
      key: "toggle",
      value: function toggle(event) {
        if (!this.$isEnabled) {
          return;
        }

        if (event) {
          this.$activeTrigger.click = !this.$activeTrigger.click;

          if (this.isWithActiveTrigger()) {
            this.enter(null);
          } else {
            this.leave(null);
          }
        } else {
          if (hasClass(this.getTipElement(), ClassName.SHOW)) {
            this.leave(null);
          } else {
            this.enter(null);
          }
        }
      } // Show tooltip

    }, {
      key: "show",
      value: function show() {
        var _this = this;

        if (!document.body.contains(this.$element) || !isVisible(this.$element)) {
          // If trigger element isn't in the DOM or is not visible
          return;
        } // Build tooltip element (also sets this.$tip)


        var tip = this.getTipElement();
        this.fixTitle();
        this.setContent(tip);

        if (!this.isWithContent(tip)) {
          // if No content, don't bother showing
          this.$tip = null;
          return;
        } // Set ID on tip and aria-describedby on element


        setAttr(tip, 'id', this.$id);
        this.addAriaDescribedby(); // Set animation on or off

        if (this.$config.animation) {
          addClass(tip, ClassName.FADE);
        } else {
          removeClass(tip, ClassName.FADE);
        }

        var placement = this.getPlacement();
        var attachment = this.constructor.getAttachment(placement);
        this.addAttachmentClass(attachment); // Create a cancelable BvEvent

        var showEvt = new BvEvent('show', {
          cancelable: true,
          target: this.$element,
          relatedTarget: tip
        });
        this.emitEvent(showEvt);

        if (showEvt.defaultPrevented) {
          // Don't show if event cancelled
          this.$tip = null;
          return;
        } // Insert tooltip if needed


        var container = this.getContainer();

        if (!document.body.contains(tip)) {
          container.appendChild(tip);
        } // Refresh popper


        this.removePopper();
        this.$popper = new Popper(this.$element, tip, this.getPopperConfig(placement, tip)); // Transitionend Callback

        var complete = function complete() {
          if (_this.$config.animation) {
            _this.fixTransition(tip);
          }

          var prevHoverState = _this.$hoverState;
          _this.$hoverState = null;

          if (prevHoverState === HoverState.OUT) {
            _this.leave(null);
          } // Create a non-cancelable BvEvent


          var shownEvt = new BvEvent('shown', {
            cancelable: false,
            target: _this.$element,
            relatedTarget: tip
          });

          _this.emitEvent(shownEvt);
        }; // Enable while open listeners/watchers


        this.setWhileOpenListeners(true); // Show tip

        addClass(tip, ClassName.SHOW); // Start the transition/animation

        this.transitionOnce(tip, complete);
      } // handler for periodic visibility check

    }, {
      key: "visibleCheck",
      value: function visibleCheck(on) {
        var _this2 = this;

        clearInterval(this.$visibleInterval);
        this.$visibleInterval = null;

        if (on) {
          this.$visibleInterval = setInterval(function () {
            var tip = _this2.getTipElement();

            if (tip && !isVisible(_this2.$element) && hasClass(tip, ClassName.SHOW)) {
              // Element is no longer visible, so force-hide the tooltip
              _this2.forceHide();
            }
          }, 100);
        }
      }
    }, {
      key: "setWhileOpenListeners",
      value: function setWhileOpenListeners(on) {
        // Modal close events
        this.setModalListener(on); // Periodic $element visibility check
        // For handling when tip is in <keepalive>, tabs, carousel, etc

        this.visibleCheck(on); // Route change events

        this.setRouteWatcher(on); // Ontouch start listeners

        this.setOnTouchStartListener(on);

        if (on && /(focus|blur)/.test(this.$config.trigger)) {
          // If focus moves between trigger element and tip container, dont close
          eventOn(this.$tip, 'focusout', this);
        } else {
          eventOff(this.$tip, 'focusout', this);
        }
      } // force hide of tip (internal method)

    }, {
      key: "forceHide",
      value: function forceHide() {
        if (!this.$tip || !hasClass(this.$tip, ClassName.SHOW)) {
          return;
        } // Disable while open listeners/watchers


        this.setWhileOpenListeners(false); // Clear any hover enter/leave event

        clearTimeout(this.$hoverTimeout);
        this.$hoverTimeout = null;
        this.$hoverState = ''; // Hide the tip

        this.hide(null, true);
      } // Hide tooltip

    }, {
      key: "hide",
      value: function hide(callback, force) {
        var _this3 = this;

        var tip = this.$tip;

        if (!tip) {
          return;
        } // Create a canelable BvEvent


        var hideEvt = new BvEvent('hide', {
          // We disable cancelling if force is true
          cancelable: !force,
          target: this.$element,
          relatedTarget: tip
        });
        this.emitEvent(hideEvt);

        if (hideEvt.defaultPrevented) {
          // Don't hide if event cancelled
          return;
        } // Transitionend Callback

        /* istanbul ignore next */


        var complete = function complete() {
          if (_this3.$hoverState !== HoverState.SHOW && tip.parentNode) {
            // Remove tip from dom, and force recompile on next show
            tip.parentNode.removeChild(tip);

            _this3.removeAriaDescribedby();

            _this3.removePopper();

            _this3.$tip = null;
          }

          if (callback) {
            callback();
          } // Create a non-cancelable BvEvent


          var hiddenEvt = new BvEvent('hidden', {
            cancelable: false,
            target: _this3.$element,
            relatedTarget: null
          });

          _this3.emitEvent(hiddenEvt);
        }; // Disable while open listeners/watchers


        this.setWhileOpenListeners(false); // If forced close, disable animation

        if (force) {
          removeClass(tip, ClassName.FADE);
        } // Hide tip


        removeClass(tip, ClassName.SHOW);
        this.$activeTrigger.click = false;
        this.$activeTrigger.focus = false;
        this.$activeTrigger.hover = false; // Start the hide transition

        this.transitionOnce(tip, complete);
        this.$hoverState = '';
      }
    }, {
      key: "emitEvent",
      value: function emitEvent(evt) {
        var evtName = evt.type;

        if (this.$root && this.$root.$emit) {
          // Emit an event on $root
          this.$root.$emit("bv::".concat(this.constructor.NAME, "::").concat(evtName), evt);
        }

        var callbacks = this.$config.callbacks || {};

        if (typeof callbacks[evtName] === 'function') {
          callbacks[evtName](evt);
        }
      }
    }, {
      key: "getContainer",
      value: function getContainer() {
        var container = this.$config.container;
        var body = document.body; // If we are in a modal, we append to the modal instead of body, unless a container is specified

        return container === false ? closest(MODAL_CLASS, this.$element) || body : select(container, body) || body;
      } // Will be overritten by popover if needed

    }, {
      key: "addAriaDescribedby",
      value: function addAriaDescribedby() {
        // Add aria-describedby on trigger element, without removing any other IDs
        var desc = getAttr(this.$element, 'aria-describedby') || '';
        desc = desc.split(/\s+/).concat(this.$id).join(' ').trim();
        setAttr(this.$element, 'aria-describedby', desc);
      } // Will be overritten by popover if needed

    }, {
      key: "removeAriaDescribedby",
      value: function removeAriaDescribedby() {
        var _this4 = this;

        var desc = getAttr(this.$element, 'aria-describedby') || '';
        desc = desc.split(/\s+/).filter(function (d) {
          return d !== _this4.$id;
        }).join(' ').trim();

        if (desc) {
          setAttr(this.$element, 'aria-describedby', desc);
        } else {
          removeAttr(this.$element, 'aria-describedby');
        }
      }
    }, {
      key: "removePopper",
      value: function removePopper() {
        if (this.$popper) {
          this.$popper.destroy();
        }

        this.$popper = null;
      }
      /* istanbul ignore next */

    }, {
      key: "transitionOnce",
      value: function transitionOnce(tip, complete) {
        var _this5 = this;

        var transEvents = this.getTransitionEndEvents();
        var called = false;
        clearTimeout(this.$fadeTimeout);
        this.$fadeTimeout = null;

        var fnOnce = function fnOnce() {
          if (called) {
            return;
          }

          called = true;
          clearTimeout(_this5.$fadeTimeout);
          _this5.$fadeTimeout = null;
          transEvents.forEach(function (evtName) {
            eventOff(tip, evtName, fnOnce);
          }); // Call complete callback

          complete();
        };

        if (hasClass(tip, ClassName.FADE)) {
          transEvents.forEach(function (evtName) {
            eventOn(tip, evtName, fnOnce);
          }); // Fallback to setTimeout

          this.$fadeTimeout = setTimeout(fnOnce, TRANSITION_DURATION);
        } else {
          fnOnce();
        }
      } // What transitionend event(s) to use? (returns array of event names)

    }, {
      key: "getTransitionEndEvents",
      value: function getTransitionEndEvents() {
        for (var name in TransitionEndEvents$1) {
          if (this.$element.style[name] !== undefined) {
            return TransitionEndEvents$1[name];
          }
        } // fallback


        return [];
      }
    }, {
      key: "update",
      value: function update() {
        if (this.$popper !== null) {
          this.$popper.scheduleUpdate();
        }
      } // NOTE: Overridden by PopOver class

    }, {
      key: "isWithContent",
      value: function isWithContent(tip) {
        tip = tip || this.$tip;

        if (!tip) {
          return false;
        }

        return Boolean((select(Selector$2.TOOLTIP_INNER, tip) || {}).innerHTML);
      } // NOTE: Overridden by PopOver class

    }, {
      key: "addAttachmentClass",
      value: function addAttachmentClass(attachment) {
        addClass(this.getTipElement(), "".concat(CLASS_PREFIX, "-").concat(attachment));
      }
    }, {
      key: "getTipElement",
      value: function getTipElement() {
        if (!this.$tip) {
          // Try and compile user supplied template, or fallback to default template
          this.$tip = this.compileTemplate(this.$config.template) || this.compileTemplate(this.constructor.Default.template);
        } // Add tab index so tip can be focused, and to allow it to be set as relatedTargt in focusin/out events


        this.$tip.tabIndex = -1;
        return this.$tip;
      }
    }, {
      key: "compileTemplate",
      value: function compileTemplate(html) {
        if (!html || typeof html !== 'string') {
          return null;
        }

        var div = document.createElement('div');
        div.innerHTML = html.trim();
        var node = div.firstElementChild ? div.removeChild(div.firstElementChild) : null;
        div = null;
        return node;
      } // NOTE: Overridden by PopOver class

    }, {
      key: "setContent",
      value: function setContent(tip) {
        this.setElementContent(select(Selector$2.TOOLTIP_INNER, tip), this.getTitle());
        removeClass(tip, ClassName.FADE);
        removeClass(tip, ClassName.SHOW);
      }
    }, {
      key: "setElementContent",
      value: function setElementContent(container, content) {
        if (!container) {
          // If container element doesn't exist, just return
          return;
        }

        var allowHtml = this.$config.html;

        if (_typeof(content) === 'object' && content.nodeType) {
          // content is a DOM node
          if (allowHtml) {
            if (content.parentElement !== container) {
              container.innerHTML = '';
              container.appendChild(content);
            }
          } else {
            container.innerText = content.innerText;
          }
        } else {
          // We have a plain HTML string or Text
          container[allowHtml ? 'innerHTML' : 'innerText'] = content;
        }
      } // NOTE: Overridden by PopOver class

    }, {
      key: "getTitle",
      value: function getTitle() {
        var title = this.$config.title || '';

        if (typeof title === 'function') {
          // Call the function to get the title value
          title = title(this.$element);
        }

        if (_typeof(title) === 'object' && title.nodeType && !title.innerHTML.trim()) {
          // We have a DOM node, but without inner content, so just return empty string
          title = '';
        }

        if (typeof title === 'string') {
          title = title.trim();
        }

        if (!title) {
          // If an explicit title is not given, try element's title attributes
          title = getAttr(this.$element, 'title') || getAttr(this.$element, 'data-original-title') || '';
          title = title.trim();
        }

        return title;
      }
    }, {
      key: "listen",
      value: function listen() {
        var _this6 = this;

        var triggers = this.$config.trigger.trim().split(/\s+/);
        var el = this.$element; // Listen for global show/hide events

        this.setRootListener(true); // Using 'this' as the handler will get automagically directed to this.handleEvent
        // And maintain our binding to 'this'

        triggers.forEach(function (trigger) {
          if (trigger === 'click') {
            eventOn(el, 'click', _this6);
          } else if (trigger === 'focus') {
            eventOn(el, 'focusin', _this6);
            eventOn(el, 'focusout', _this6);
          } else if (trigger === 'blur') {
            // Used to close $tip when element looses focus
            eventOn(el, 'focusout', _this6);
          } else if (trigger === 'hover') {
            eventOn(el, 'mouseenter', _this6);
            eventOn(el, 'mouseleave', _this6);
          }
        }, this);
      }
    }, {
      key: "unListen",
      value: function unListen() {
        var _this7 = this;

        var events = ['click', 'focusin', 'focusout', 'mouseenter', 'mouseleave']; // Using "this" as the handler will get automagically directed to this.handleEvent

        events.forEach(function (evt) {
          eventOff(_this7.$element, evt, _this7);
        }, this); // Stop listening for global show/hide/enable/disable events

        this.setRootListener(false);
      }
    }, {
      key: "handleEvent",
      value: function handleEvent(e) {
        // This special method allows us to use "this" as the event handlers
        if (isDisabled(this.$element)) {
          // If disabled, don't do anything. Note: if tip is shown before element gets
          // disabled, then tip not close until no longer disabled or forcefully closed.
          return;
        }

        if (!this.$isEnabled) {
          // If not enable
          return;
        }

        var type = e.type;
        var target = e.target;
        var relatedTarget = e.relatedTarget;
        var $element = this.$element;
        var $tip = this.$tip;

        if (type === 'click') {
          this.toggle(e);
        } else if (type === 'focusin' || type === 'mouseenter') {
          this.enter(e);
        } else if (type === 'focusout') {
          // target is the element which is loosing focus
          // And relatedTarget is the element gaining focus
          if ($tip && $element && $element.contains(target) && $tip.contains(relatedTarget)) {
            // If focus moves from $element to $tip, don't trigger a leave
            return;
          }

          if ($tip && $element && $tip.contains(target) && $element.contains(relatedTarget)) {
            // If focus moves from $tip to $element, don't trigger a leave
            return;
          }

          if ($tip && $tip.contains(target) && $tip.contains(relatedTarget)) {
            // If focus moves within $tip, don't trigger a leave
            return;
          }

          if ($element && $element.contains(target) && $element.contains(relatedTarget)) {
            // If focus moves within $element, don't trigger a leave
            return;
          } // Otherwise trigger a leave


          this.leave(e);
        } else if (type === 'mouseleave') {
          this.leave(e);
        }
      }
      /* istanbul ignore next */

    }, {
      key: "setRouteWatcher",
      value: function setRouteWatcher(on) {
        var _this8 = this;

        if (on) {
          this.setRouteWatcher(false);

          if (this.$root && Boolean(this.$root.$route)) {
            this.$routeWatcher = this.$root.$watch('$route', function (newVal, oldVal) {
              if (newVal === oldVal) {
                return;
              } // If route has changed, we force hide the tooltip/popover


              _this8.forceHide();
            });
          }
        } else {
          if (this.$routeWatcher) {
            // cancel the route watcher by calling the stored reference
            this.$routeWatcher();
            this.$routeWatcher = null;
          }
        }
      }
      /* istanbul ignore next */

    }, {
      key: "setModalListener",
      value: function setModalListener(on) {
        var modal = closest(MODAL_CLASS, this.$element);

        if (!modal) {
          // If we are not in a modal, don't worry. be happy
          return;
        } // We can listen for modal hidden events on $root


        if (this.$root) {
          this.$root[on ? '$on' : '$off'](MODAL_CLOSE_EVENT, this.$forceHide);
        }
      }
      /* istanbul ignore next */

    }, {
      key: "setRootListener",
      value: function setRootListener(on) {
        // Listen for global 'bv::{hide|show}::{tooltip|popover}' hide request event
        if (this.$root) {
          this.$root[on ? '$on' : '$off']("bv::hide::".concat(this.constructor.NAME), this.$doHide);
          this.$root[on ? '$on' : '$off']("bv::show::".concat(this.constructor.NAME), this.$doShow);
          this.$root[on ? '$on' : '$off']("bv::disable::".concat(this.constructor.NAME), this.$doDisable);
          this.$root[on ? '$on' : '$off']("bv::enable::".concat(this.constructor.NAME), this.$doEnable);
        }
      }
    }, {
      key: "doHide",
      value: function doHide(id) {
        // Programmatically hide tooltip or popover
        if (!id) {
          // Close all tooltips or popovers
          this.forceHide();
        } else if (this.$element && this.$element.id && this.$element.id === id) {
          // Close this specific tooltip or popover
          this.hide();
        }
      }
    }, {
      key: "doShow",
      value: function doShow(id) {
        // Programmatically show tooltip or popover
        if (!id) {
          // Open all tooltips or popovers
          this.show();
        } else if (id && this.$element && this.$element.id && this.$element.id === id) {
          // Show this specific tooltip or popover
          this.show();
        }
      }
    }, {
      key: "doDisable",
      value: function doDisable(id) {
        // Programmatically disable tooltip or popover
        if (!id) {
          // Disable all tooltips or popovers
          this.disable();
        } else if (this.$element && this.$element.id && this.$element.id === id) {
          // Disable this specific tooltip or popover
          this.disable();
        }
      }
    }, {
      key: "doEnable",
      value: function doEnable(id) {
        // Programmatically enable tooltip or popover
        if (!id) {
          // Enable all tooltips or popovers
          this.enable();
        } else if (this.$element && this.$element.id && this.$element.id === id) {
          // Enable this specific tooltip or popover
          this.enable();
        }
      }
      /* istanbul ignore next */

    }, {
      key: "setOnTouchStartListener",
      value: function setOnTouchStartListener(on) {
        var _this9 = this;

        // if this is a touch-enabled device we add extra
        // empty mouseover listeners to the body's immediate children;
        // only needed because of broken event delegation on iOS
        // https://www.quirksmode.org/blog/archives/2014/02/mouse_event_bub.html
        if ('ontouchstart' in document.documentElement) {
          from(document.body.children).forEach(function (el) {
            if (on) {
              eventOn(el, 'mouseover', _this9._noop);
            } else {
              eventOff(el, 'mouseover', _this9._noop);
            }
          });
        }
      }
      /* istanbul ignore next */

    }, {
      key: "_noop",
      value: function _noop() {// Empty noop handler for ontouchstart devices
      }
    }, {
      key: "fixTitle",
      value: function fixTitle() {
        var el = this.$element;

        var titleType = _typeof(getAttr(el, 'data-original-title'));

        if (getAttr(el, 'title') || titleType !== 'string') {
          setAttr(el, 'data-original-title', getAttr(el, 'title') || '');
          setAttr(el, 'title', '');
        }
      } // Enter handler

      /* istanbul ignore next */

    }, {
      key: "enter",
      value: function enter(e) {
        var _this10 = this;

        if (e) {
          this.$activeTrigger[e.type === 'focusin' ? 'focus' : 'hover'] = true;
        }

        if (hasClass(this.getTipElement(), ClassName.SHOW) || this.$hoverState === HoverState.SHOW) {
          this.$hoverState = HoverState.SHOW;
          return;
        }

        clearTimeout(this.$hoverTimeout);
        this.$hoverState = HoverState.SHOW;

        if (!this.$config.delay || !this.$config.delay.show) {
          this.show();
          return;
        }

        this.$hoverTimeout = setTimeout(function () {
          if (_this10.$hoverState === HoverState.SHOW) {
            _this10.show();
          }
        }, this.$config.delay.show);
      } // Leave handler

      /* istanbul ignore next */

    }, {
      key: "leave",
      value: function leave(e) {
        var _this11 = this;

        if (e) {
          this.$activeTrigger[e.type === 'focusout' ? 'focus' : 'hover'] = false;

          if (e.type === 'focusout' && /blur/.test(this.$config.trigger)) {
            // Special case for `blur`: we clear out the other triggers
            this.$activeTrigger.click = false;
            this.$activeTrigger.hover = false;
          }
        }

        if (this.isWithActiveTrigger()) {
          return;
        }

        clearTimeout(this.$hoverTimeout);
        this.$hoverState = HoverState.OUT;

        if (!this.$config.delay || !this.$config.delay.hide) {
          this.hide();
          return;
        }

        this.$hoverTimeout = setTimeout(function () {
          if (_this11.$hoverState === HoverState.OUT) {
            _this11.hide();
          }
        }, this.$config.delay.hide);
      }
    }, {
      key: "getPopperConfig",
      value: function getPopperConfig(placement, tip) {
        var _this12 = this;

        return {
          placement: this.constructor.getAttachment(placement),
          modifiers: {
            offset: {
              offset: this.getOffset(placement, tip)
            },
            flip: {
              behavior: this.$config.fallbackPlacement
            },
            arrow: {
              element: '.arrow'
            },
            preventOverflow: {
              padding: this.$config.boundaryPadding,
              boundariesElement: this.$config.boundary
            }
          },
          onCreate: function onCreate(data) {
            // Handle flipping arrow classes
            if (data.originalPlacement !== data.placement) {
              _this12.handlePopperPlacementChange(data);
            }
          },
          onUpdate: function onUpdate(data) {
            // Handle flipping arrow classes
            _this12.handlePopperPlacementChange(data);
          }
        };
      }
    }, {
      key: "getOffset",
      value: function getOffset(placement, tip) {
        if (!this.$config.offset) {
          var arrow = select(Selector$2.ARROW, tip);
          var arrowOffset = parseFloat(getCS(arrow).width) + parseFloat(this.$config.arrowPadding);

          switch (OffsetMap[placement.toUpperCase()]) {
            case +1:
              return "+50%p - ".concat(arrowOffset, "px");

            case -1:
              return "-50%p + ".concat(arrowOffset, "px");

            default:
              return 0;
          }
        }

        return this.$config.offset;
      }
    }, {
      key: "getPlacement",
      value: function getPlacement() {
        var placement = this.$config.placement;

        if (typeof placement === 'function') {
          return placement.call(this, this.$tip, this.$element);
        }

        return placement;
      }
    }, {
      key: "isWithActiveTrigger",
      value: function isWithActiveTrigger() {
        for (var trigger in this.$activeTrigger) {
          if (this.$activeTrigger[trigger]) {
            return true;
          }
        }

        return false;
      } // NOTE: Overridden by PopOver class

    }, {
      key: "cleanTipClass",
      value: function cleanTipClass() {
        var tip = this.getTipElement();
        var tabClass = tip.className.match(BSCLS_PREFIX_REGEX);

        if (tabClass !== null && tabClass.length > 0) {
          tabClass.forEach(function (cls) {
            removeClass(tip, cls);
          });
        }
      }
    }, {
      key: "handlePopperPlacementChange",
      value: function handlePopperPlacementChange(data) {
        this.cleanTipClass();
        this.addAttachmentClass(this.constructor.getAttachment(data.placement));
      }
    }, {
      key: "fixTransition",
      value: function fixTransition(tip) {
        var initConfigAnimation = this.$config.animation || false;

        if (getAttr(tip, 'x-placement') !== null) {
          return;
        }

        removeClass(tip, ClassName.FADE);
        this.$config.animation = false;
        this.hide();
        this.show();
        this.$config.animation = initConfigAnimation;
      }
    }], [{
      key: "getAttachment",
      value: function getAttachment(placement) {
        return AttachmentMap$1[placement.toUpperCase()];
      }
    }, {
      key: "Default",
      get: function get() {
        return Defaults$1;
      } // NOTE: Overridden by PopOver class

    }, {
      key: "NAME",
      get: function get() {
        return NAME;
      }
    }]);

    return ToolTip;
  }();

  var NAME$1 = 'popover';
  var CLASS_PREFIX$1 = 'bs-popover';
  var BSCLS_PREFIX_REGEX$1 = new RegExp("\\b".concat(CLASS_PREFIX$1, "\\S+"), 'g');

  var Defaults$2 = _objectSpread({}, ToolTip.Default, {
    placement: 'right',
    trigger: 'click',
    content: '',
    template: '<div class="popover" role="tooltip">' + '<div class="arrow"></div>' + '<h3 class="popover-header"></h3>' + '<div class="popover-body"></div></div>'
  });

  var ClassName$1 = {
    FADE: 'fade',
    SHOW: 'show'
  };
  var Selector$3 = {
    TITLE: '.popover-header',
    CONTENT: '.popover-body'
    /* istanbul ignore next: dificult to test in Jest/JSDOM environment */

  };

  var PopOver =
  /*#__PURE__*/
  function (_ToolTip) {
    _inherits(PopOver, _ToolTip);

    function PopOver() {
      _classCallCheck(this, PopOver);

      return _possibleConstructorReturn(this, _getPrototypeOf(PopOver).apply(this, arguments));
    }

    _createClass(PopOver, [{
      key: "isWithContent",
      // Method overrides
      value: function isWithContent(tip) {
        tip = tip || this.$tip;

        if (!tip) {
          return false;
        }

        var hasTitle = Boolean((select(Selector$3.TITLE, tip) || {}).innerHTML);
        var hasContent = Boolean((select(Selector$3.CONTENT, tip) || {}).innerHTML);
        return hasTitle || hasContent;
      }
    }, {
      key: "addAttachmentClass",
      value: function addAttachmentClass(attachment) {
        addClass(this.getTipElement(), "".concat(CLASS_PREFIX$1, "-").concat(attachment));
      }
    }, {
      key: "setContent",
      value: function setContent(tip) {
        // we use append for html objects to maintain js events/components
        this.setElementContent(select(Selector$3.TITLE, tip), this.getTitle());
        this.setElementContent(select(Selector$3.CONTENT, tip), this.getContent());
        removeClass(tip, ClassName$1.FADE);
        removeClass(tip, ClassName$1.SHOW);
      } // This method may look identical to ToolTip version, but it uses a different RegEx defined above

    }, {
      key: "cleanTipClass",
      value: function cleanTipClass() {
        var tip = this.getTipElement();
        var tabClass = tip.className.match(BSCLS_PREFIX_REGEX$1);

        if (tabClass !== null && tabClass.length > 0) {
          tabClass.forEach(function (cls) {
            removeClass(tip, cls);
          });
        }
      }
    }, {
      key: "getTitle",
      value: function getTitle() {
        var title = this.$config.title || '';

        if (typeof title === 'function') {
          title = title(this.$element);
        }

        if (_typeof(title) === 'object' && title.nodeType && !title.innerHTML.trim()) {
          // We have a dom node, but without inner content, so just return an empty string
          title = '';
        }

        if (typeof title === 'string') {
          title = title.trim();
        }

        if (!title) {
          // Try and grab element's title attribute
          title = getAttr(this.$element, 'title') || getAttr(this.$element, 'data-original-title') || '';
          title = title.trim();
        }

        return title;
      } // New methods

    }, {
      key: "getContent",
      value: function getContent() {
        var content = this.$config.content || '';

        if (typeof content === 'function') {
          content = content(this.$element);
        }

        if (_typeof(content) === 'object' && content.nodeType && !content.innerHTML.trim()) {
          // We have a dom node, but without inner content, so just return an empty string
          content = '';
        }

        if (typeof content === 'string') {
          content = content.trim();
        }

        return content;
      }
    }], [{
      key: "Default",
      // Getter overrides
      get: function get() {
        return Defaults$2;
      }
    }, {
      key: "NAME",
      get: function get() {
        return NAME$1;
      }
    }]);

    return PopOver;
  }(ToolTip);

  // Polyfills for SSR
  var isSSR = typeof window === 'undefined';
  var HTMLElement = isSSR ? Object : window.HTMLElement;

  var PLACEMENTS = {
    top: 'top',
    topleft: 'topleft',
    topright: 'topright',
    right: 'right',
    righttop: 'righttop',
    rightbottom: 'rightbottom',
    bottom: 'bottom',
    bottomleft: 'bottomleft',
    bottomright: 'bottomright',
    left: 'left',
    lefttop: 'lefttop',
    leftbottom: 'leftbottom',
    auto: 'auto'
  };
  var OBSERVER_CONFIG$1 = {
    subtree: true,
    childList: true,
    characterData: true,
    attributes: true,
    attributeFilter: ['class', 'style'] // @vue/component

  };
  var toolpopMixin = {
    props: {
      target: {
        // String ID of element, or element/component reference
        type: [String, Object, HTMLElement, Function] // default: undefined

      },
      delay: {
        type: [Number, Object, String],
        default: 0
      },
      offset: {
        type: [Number, String],
        default: 0
      },
      noFade: {
        type: Boolean,
        default: false
      },
      container: {
        // String ID of container, if null body is used (default)
        type: String,
        default: null
      },
      boundary: {
        // String: scrollParent, window, or viewport
        // Element: element reference
        type: [String, HTMLElement],
        default: 'scrollParent'
      },
      boundaryPadding: {
        type: Number,
        default: 5
      },
      show: {
        type: Boolean,
        default: false
      },
      disabled: {
        type: Boolean,
        default: false
      }
    },
    computed: {
      baseConfig: function baseConfig() {
        var cont = this.container;
        var delay = _typeof(this.delay) === 'object' ? this.delay : parseInt(this.delay, 10) || 0;
        return {
          // Title prop
          title: (this.title || '').trim() || '',
          // Contnt prop (if popover)
          content: (this.content || '').trim() || '',
          // Tooltip/Popover placement
          placement: PLACEMENTS[this.placement] || 'auto',
          // Container curently needs to be an ID with '#' prepended, if null then body is used
          container: cont ? /^#/.test(cont) ? cont : "#".concat(cont) : false,
          // boundariesElement passed to popper
          boundary: this.boundary,
          // boundariesElement padding passed to popper
          boundaryPadding: this.boundaryPadding,
          // Show/Hide delay
          delay: delay || 0,
          // Offset can be css distance. if no units, pixels are assumed
          offset: this.offset || 0,
          // Disable fade Animation?
          animation: !this.noFade,
          // Open/Close Trigger(s)
          trigger: isArray(this.triggers) ? this.triggers.join(' ') : this.triggers,
          // Callbacks so we can trigger events on component
          callbacks: {
            show: this.onShow,
            shown: this.onShown,
            hide: this.onHide,
            hidden: this.onHidden,
            enabled: this.onEnabled,
            disabled: this.onDisabled
          }
        };
      }
    },
    watch: {
      show: function show(_show, old) {
        if (_show === old) {
          return;
        }

        _show ? this.onOpen() : this.onClose();
      },
      disabled: function disabled(_disabled, old) {
        if (_disabled === old) {
          return;
        }

        _disabled ? this.onDisable() : this.onEnable();
      }
    },
    created: function created() {
      // Create non-reactive property
      this._toolpop = null;
      this._obs_title = null;
      this._obs_content = null;
    },
    mounted: function mounted() {
      var _this = this;

      // We do this in a next tick to ensure DOM has rendered first
      this.$nextTick(function () {
        // Instantiate ToolTip/PopOver on target
        // The createToolpop method must exist in main component
        if (_this.createToolpop()) {
          if (_this.disabled) {
            // Initially disabled
            _this.onDisable();
          } // Listen to open signals from others


          _this.$on('open', _this.onOpen); // Listen to close signals from others


          _this.$on('close', _this.onClose); // Listen to disable signals from others


          _this.$on('disable', _this.onDisable); // Listen to disable signals from others


          _this.$on('enable', _this.onEnable); // Observe content Child changes so we can notify popper of possible size change


          _this.setObservers(true); // Set intially open state


          if (_this.show) {
            _this.onOpen();
          }
        }
      });
    },
    updated: function updated() {
      // If content/props changes, etc

      /* istanbul ignore if: can't test in JSDOM */
      if (this._toolpop) {
        this._toolpop.updateConfig(this.getConfig());
      }
    },
    activated: function activated() {
      // Called when component is inside a <keep-alive> and component brought offline

      /* istanbul ignore next: can't test in JSDOM */
      this.setObservers(true);
    },
    deactivated: function deactivated() {
      // Called when component is inside a <keep-alive> and component taken offline

      /* istanbul ignore if: can't test in JSDOM */
      if (this._toolpop) {
        this.setObservers(false);

        this._toolpop.hide();
      }
    },
    beforeDestroy: function beforeDestroy()
    /* istanbul ignore next: not easy to test */
    {
      // Shutdown our local event listeners
      this.$off('open', this.onOpen);
      this.$off('close', this.onClose);
      this.$off('disable', this.onDisable);
      this.$off('enable', this.onEnable);
      this.setObservers(false); // bring our content back if needed

      this.bringItBack();

      if (this._toolpop) {
        this._toolpop.destroy();

        this._toolpop = null;
      }
    },
    methods: {
      getConfig: function getConfig() {
        var cfg = _objectSpread({}, this.baseConfig);

        if (this.$refs.title && this.$refs.title.innerHTML.trim()) {
          // If slot has content, it overrides 'title' prop
          // We use the DOM node as content to allow components!
          cfg.title = this.$refs.title;
          cfg.html = true;
        }

        if (this.$refs.content && this.$refs.content.innerHTML.trim()) {
          // If slot has content, it overrides 'content' prop
          // We use the DOM node as content to allow components!
          cfg.content = this.$refs.content;
          cfg.html = true;
        }

        return cfg;
      },
      onOpen: function onOpen() {
        if (this._toolpop) {
          this._toolpop.show();
        }
      },
      onClose: function onClose(callback) {
        if (this._toolpop) {
          this._toolpop.hide(callback);
        } else if (typeof callback === 'function') {
          callback();
        }
      },
      onDisable: function onDisable() {
        /* istanbul ignore if: can't test in JSDOM */
        if (this._toolpop) {
          this._toolpop.disable();
        }
      },
      onEnable: function onEnable() {
        /* istanbul ignore if: can't test in JSDOM */
        if (this._toolpop) {
          this._toolpop.enable();
        }
      },
      updatePosition: function updatePosition() {
        /* istanbul ignore if: can't test in JSDOM */
        if (this._toolpop) {
          // Instruct popper to reposition popover if necessary
          this._toolpop.update();
        }
      },
      getTarget: function getTarget() {
        var target = this.target;

        if (typeof target === 'function') {
          target = target();
        }

        if (typeof target === 'string') {
          // Assume ID of element
          return getById(target);
        } else if (_typeof(target) === 'object' && isElement(target.$el)) {
          // Component reference
          return target.$el;
        } else if (_typeof(target) === 'object' && isElement(target)) {
          // Element reference
          return target;
        }

        return null;
      },
      onShow: function onShow(evt) {
        this.$emit('show', evt);
      },
      onShown: function onShown(evt) {
        this.setObservers(true);
        this.$emit('update:show', true);
        this.$emit('shown', evt);
      },
      onHide: function onHide(evt) {
        this.$emit('hide', evt);
      },
      onHidden: function onHidden(evt) {
        this.setObservers(false); // bring our content back if needed to keep Vue happy
        // Tooltip class will move it back to tip when shown again

        this.bringItBack();
        this.$emit('update:show', false);
        this.$emit('hidden', evt);
      },
      onEnabled: function onEnabled(evt) {
        if (!evt || evt.type !== 'enabled') {
          // Prevent possible endless loop if user mistakienly fires enabled instead of enable
          return;
        }

        this.$emit('update:disabled', false);
        this.$emit('disabled');
      },
      onDisabled: function onDisabled(evt) {
        if (!evt || evt.type !== 'disabled') {
          // Prevent possible endless loop if user mistakienly fires disabled instead of disable
          return;
        }

        this.$emit('update:disabled', true);
        this.$emit('enabled');
      },
      bringItBack: function bringItBack() {
        // bring our content back if needed to keep Vue happy
        if (this.$el && this.$refs.title) {
          this.$el.appendChild(this.$refs.title);
        }

        if (this.$el && this.$refs.content) {
          this.$el.appendChild(this.$refs.content);
        }
      },
      setObservers: function setObservers(on)
      /* istanbul ignore next: can't test in JSDOM */
      {
        if (on) {
          if (this.$refs.title) {
            this._obs_title = observeDOM(this.$refs.title, this.updatePosition.bind(this), OBSERVER_CONFIG$1);
          }

          if (this.$refs.content) {
            this._obs_content = observeDOM(this.$refs.content, this.updatePosition.bind(this), OBSERVER_CONFIG$1);
          }
        } else {
          if (this._obs_title) {
            this._obs_title.disconnect();

            this._obs_title = null;
          }

          if (this._obs_content) {
            this._obs_content.disconnect();

            this._obs_content = null;
          }
        }
      }
    }
  };

  var BPopover = {
    name: 'BPopover',
    mixins: [toolpopMixin],
    props: {
      title: {
        type: String,
        default: ''
      },
      content: {
        type: String,
        default: ''
      },
      triggers: {
        type: [String, Array],
        default: 'click'
      },
      placement: {
        type: String,
        default: 'right'
      }
    },
    data: function data() {
      return {};
    },
    methods: {
      createToolpop: function createToolpop() {
        // getTarget is in toolpop mixin
        var target = this.getTarget();

        if (target) {
          this._toolpop = new PopOver(target, this.getConfig(), this.$root);
        } else {
          this._toolpop = null;
          warn("b-popover: 'target' element not found!");
        }

        return this._toolpop;
      }
    },
    render: function render(h) {
      return h('div', {
        class: ['d-none'],
        style: {
          display: 'none'
        },
        attrs: {
          'aria-hidden': true
        }
      }, [h('div', {
        ref: 'title'
      }, this.$slots.title), h('div', {
        ref: 'content'
      }, this.$slots.default)]);
    }
  };

  var inBrowser$2 = typeof window !== 'undefined' && typeof document !== 'undefined'; // Key which we use to store tooltip object on element

  var BVPO = '__BV_PopOver__'; // Valid event triggers

  var validTriggers = {
    focus: true,
    hover: true,
    click: true,
    blur: true // Build a PopOver config based on bindings (if any)
    // Arguments and modifiers take precedence over pased value config object

    /* istanbul ignore next: not easy to test */

  };

  function parseBindings(bindings) {
    // We start out with a blank config
    var config = {}; // Process bindings.value

    if (typeof bindings.value === 'string') {
      // Value is popover content (html optionally supported)
      config.content = bindings.value;
    } else if (typeof bindings.value === 'function') {
      // Content generator function
      config.content = bindings.value;
    } else if (_typeof(bindings.value) === 'object') {
      // Value is config object, so merge
      config = _objectSpread({}, config, bindings.value);
    } // If Argument, assume element ID of container element


    if (bindings.arg) {
      // Element ID specified as arg. We must prepend '#' to become a CSS selector
      config.container = "#".concat(bindings.arg);
    } // Process modifiers


    keys(bindings.modifiers).forEach(function (mod) {
      if (/^html$/.test(mod)) {
        // Title allows HTML
        config.html = true;
      } else if (/^nofade$/.test(mod)) {
        // no animation
        config.animation = false;
      } else if (/^(auto|top(left|right)?|bottom(left|right)?|left(top|bottom)?|right(top|bottom)?)$/.test(mod)) {
        // placement of popover
        config.placement = mod;
      } else if (/^(window|viewport)$/.test(mod)) {
        // bounday of popover
        config.boundary = mod;
      } else if (/^d\d+$/.test(mod)) {
        // delay value
        var delay = parseInt(mod.slice(1), 10) || 0;

        if (delay) {
          config.delay = delay;
        }
      } else if (/^o-?\d+$/.test(mod)) {
        // offset value (negative allowed)
        var offset = parseInt(mod.slice(1), 10) || 0;

        if (offset) {
          config.offset = offset;
        }
      }
    }); // Special handling of event trigger modifiers Trigger is a space separated list

    var selectedTriggers = {}; // parse current config object trigger

    var triggers = typeof config.trigger === 'string' ? config.trigger.trim().split(/\s+/) : [];
    triggers.forEach(function (trigger) {
      if (validTriggers[trigger]) {
        selectedTriggers[trigger] = true;
      }
    }); // Parse Modifiers for triggers

    keys(validTriggers).forEach(function (trigger) {
      if (bindings.modifiers[trigger]) {
        selectedTriggers[trigger] = true;
      }
    }); // Sanitize triggers

    config.trigger = keys(selectedTriggers).join(' ');

    if (config.trigger === 'blur') {
      // Blur by itself is useless, so convert it to focus
      config.trigger = 'focus';
    }

    if (!config.trigger) {
      // remove trigger config
      delete config.trigger;
    }

    return config;
  } //
  // Add or Update popover on our element
  //

  /* istanbul ignore next: not easy to test */


  function applyBVPO(el, bindings, vnode) {
    if (!inBrowser$2) {
      return;
    }

    if (!Popper) {
      // Popper is required for tooltips to work
      warn('v-b-popover: Popper.js is required for popovers to work');
      return;
    }

    if (el[BVPO]) {
      el[BVPO].updateConfig(parseBindings(bindings));
    } else {
      el[BVPO] = new PopOver(el, parseBindings(bindings), vnode.context.$root);
    }
  } //
  // Remove popover on our element
  //

  /* istanbul ignore next */


  function removeBVPO(el) {
    if (!inBrowser$2) {
      return;
    }

    if (el[BVPO]) {
      el[BVPO].destroy();
      el[BVPO] = null;
      delete el[BVPO];
    }
  }
  /*
   * Export our directive
   */

  /* istanbul ignore next: not easy to test */


  var bPopover = {
    bind: function bind(el, bindings, vnode) {
      applyBVPO(el, bindings, vnode);
    },
    inserted: function inserted(el, bindings, vnode) {
      applyBVPO(el, bindings, vnode);
    },
    update: function update(el, bindings, vnode) {
      if (bindings.value !== bindings.oldValue) {
        applyBVPO(el, bindings, vnode);
      }
    },
    componentUpdated: function componentUpdated(el, bindings, vnode) {
      if (bindings.value !== bindings.oldValue) {
        applyBVPO(el, bindings, vnode);
      }
    },
    unbind: function unbind(el) {
      removeBVPO(el);
    }
  };

  var directives$2 = {
    bPopover: bPopover
  };
  var popoverDirectivePlugin = {
    install: function install(Vue) {
      registerDirectives(Vue, directives$2);
    }
  };

  var components$v = {
    BPopover: BPopover
  };
  var index$s = {
    install: function install(Vue) {
      registerComponents(Vue, components$v);
      Vue.use(popoverDirectivePlugin);
    }
  };

  var BProgressBar = {
    name: 'BProgressBar',
    inject: {
      progress: {
        from: 'progress',
        default: function _default() {
          return {};
        }
      }
    },
    props: {
      value: {
        type: Number,
        default: 0
      },
      label: {
        type: String,
        default: null
      },
      labelHtml: {
        type: String
      },
      // $parent prop values take precedence over the following props
      // Which is why they are defaulted to null
      max: {
        type: Number,
        default: null
      },
      precision: {
        type: Number,
        default: null
      },
      variant: {
        type: String,
        default: null
      },
      striped: {
        type: Boolean,
        default: null
      },
      animated: {
        type: Boolean,
        default: null
      },
      showProgress: {
        type: Boolean,
        default: null
      },
      showValue: {
        type: Boolean,
        default: null
      }
    },
    computed: {
      progressBarClasses: function progressBarClasses() {
        return [this.computedVariant ? "bg-".concat(this.computedVariant) : '', this.computedStriped || this.computedAnimated ? 'progress-bar-striped' : '', this.computedAnimated ? 'progress-bar-animated' : ''];
      },
      progressBarStyles: function progressBarStyles() {
        return {
          width: 100 * (this.value / this.computedMax) + '%'
        };
      },
      computedProgress: function computedProgress() {
        var p = Math.pow(10, this.computedPrecision);
        return Math.round(100 * p * this.value / this.computedMax) / p;
      },
      computedMax: function computedMax() {
        // Prefer our max over parent setting
        return typeof this.max === 'number' ? this.max : this.progress.max || 100;
      },
      computedVariant: function computedVariant() {
        // Prefer our variant over parent setting
        return this.variant || this.progress.variant;
      },
      computedPrecision: function computedPrecision() {
        // Prefer our precision over parent setting
        return typeof this.precision === 'number' ? this.precision : this.progress.precision || 0;
      },
      computedStriped: function computedStriped() {
        // Prefer our striped over parent setting
        return typeof this.striped === 'boolean' ? this.striped : this.progress.striped || false;
      },
      computedAnimated: function computedAnimated() {
        // Prefer our animated over parent setting
        return typeof this.animated === 'boolean' ? this.animated : this.progress.animated || false;
      },
      computedShowProgress: function computedShowProgress() {
        // Prefer our showProgress over parent setting
        return typeof this.showProgress === 'boolean' ? this.showProgress : this.progress.showProgress || false;
      },
      computedShowValue: function computedShowValue() {
        // Prefer our showValue over parent setting
        return typeof this.showValue === 'boolean' ? this.showValue : this.progress.showValue || false;
      }
    },
    render: function render(h) {
      var childNodes = h(false);

      if (this.$slots.default) {
        childNodes = this.$slots.default;
      } else if (this.label || this.labelHtml) {
        childNodes = h('span', {
          domProps: htmlOrText(this.labelHtml, this.label)
        });
      } else if (this.computedShowProgress) {
        childNodes = this.computedProgress.toFixed(this.computedPrecision);
      } else if (this.computedShowValue) {
        childNodes = this.value.toFixed(this.computedPrecision);
      }

      return h('div', {
        staticClass: 'progress-bar',
        class: this.progressBarClasses,
        style: this.progressBarStyles,
        attrs: {
          role: 'progressbar',
          'aria-valuemin': '0',
          'aria-valuemax': this.computedMax.toString(),
          'aria-valuenow': this.value.toFixed(this.computedPrecision)
        }
      }, [childNodes]);
    }
  };

  var BProgress = {
    name: 'BProgress',
    components: {
      BProgressBar: BProgressBar
    },
    provide: function provide() {
      return {
        progress: this
      };
    },
    props: {
      // These props can be inherited via the child b-progress-bar(s)
      variant: {
        type: String,
        default: null
      },
      striped: {
        type: Boolean,
        default: false
      },
      animated: {
        type: Boolean,
        default: false
      },
      height: {
        type: String,
        default: null
      },
      precision: {
        type: Number,
        default: 0
      },
      showProgress: {
        type: Boolean,
        default: false
      },
      showValue: {
        type: Boolean,
        default: false
      },
      max: {
        type: Number,
        default: 100
      },
      // This prop is not inherited by child b-progress-bar(s)
      value: {
        type: Number,
        default: 0
      }
    },
    computed: {
      progressHeight: function progressHeight() {
        return {
          height: this.height || null
        };
      }
    },
    render: function render(h) {
      var childNodes = this.$slots.default;

      if (!childNodes) {
        childNodes = h('b-progress-bar', {
          props: {
            value: this.value,
            max: this.max,
            precision: this.precision,
            variant: this.variant,
            animated: this.animated,
            striped: this.striped,
            showProgress: this.showProgress,
            showValue: this.showValue
          }
        });
      }

      return h('div', {
        class: ['progress'],
        style: this.progressHeight
      }, [childNodes]);
    }
  };

  var components$w = {
    BProgress: BProgress,
    BProgressBar: BProgressBar
  };
  var index$t = {
    install: function install(Vue) {
      registerComponents(Vue, components$w);
    }
  };

  var BSpinner = {
    name: 'BSpinner',
    functional: true,
    props: {
      type: {
        type: String,
        default: 'border' // SCSS currently supports 'border' or 'grow'

      },
      label: {
        type: String,
        default: null
      },
      variant: {
        type: String,
        default: null
      },
      small: {
        type: Boolean,
        default: false
      },
      role: {
        type: String,
        default: 'status'
      },
      tag: {
        type: String,
        default: 'span'
      }
    },
    render: function render(h, _ref) {
      var _class;

      var props = _ref.props,
          data = _ref.data,
          slots = _ref.slots;
      var label = h(false);
      var hasLabel = slots().label || props.label;

      if (hasLabel) {
        label = h('span', {
          staticClass: 'sr-only'
        }, hasLabel);
      }

      return h(props.tag, mergeData(data, {
        attrs: {
          role: hasLabel ? props.role || 'status' : null,
          'aria-hidden': hasLabel ? null : 'true'
        },
        class: (_class = {}, _defineProperty(_class, "spinner-".concat(props.type), Boolean(props.type)), _defineProperty(_class, "spinner-".concat(props.type, "-sm"), props.small), _defineProperty(_class, "text-".concat(props.variant), Boolean(props.variant)), _class)
      }), [label]);
    }
  };

  var components$x = {
    BSpinner: BSpinner
  };
  var index$u = {
    install: function install(Vue) {
      registerComponents(Vue, components$x);
    }
  };

  /**
   * Converts a string, including strings in camelCase or snake_case, into Start Case (a variant
   * of Title Case where all words start with a capital letter), it keeps original single quote
   * and hyphen in the word.
   *
   * Copyright (c) 2017 Compass (MIT)
   * https://github.com/UrbanCompass/to-start-case
   * @author Zhuoyuan Zhang <https://github.com/drawyan>
   * @author Wei Wang <https://github.com/onlywei>
   *
   *
   *   'management_companies' to 'Management Companies'
   *   'managementCompanies' to 'Management Companies'
   *   `hell's kitchen` to `Hell's Kitchen`
   *   `co-op` to `Co-op`
   *
   * @param {String} str
   * @returns {String}
   */
  function toStartCaseStr(str) {
    return str.replace(/_/g, ' ').replace(/([a-z])([A-Z])/g, function (str, $1, $2) {
      return $1 + ' ' + $2;
    }).replace(/(\s|^)(\w)/g, function (str, $1, $2) {
      return $1 + $2.toUpperCase();
    });
  }

  /**
   * Get property defined by dot notation in string.
   *
   * Copyright (C) 2014 (UNLICENSE)
   * @author Dmitry Yv <https://github.com/dy>
   *
   * @param  {Object} holder   Target object where to look property up
   * @param  {string} propName Dot notation, like 'this.a.b.c'
   * @return {*}          A property value
   */
  function get(holder, propName) {
    if (propName === undefined) {
      return holder;
    }

    var propParts = (propName + '').split('.');
    var result = holder;
    var lastPropName;

    while ((lastPropName = propParts.shift()) !== undefined && // Fix for https://github.com/bootstrap-vue/bootstrap-vue/issues/2623
    result !== undefined && result !== null) {
      if (result[lastPropName] === undefined) return undefined;
      result = result[lastPropName];
    }

    return result;
  }

  /*
   * Consitant and stable sort function across JavsaScript platforms
   *
   * Inconsistent sorts can cause SSR problems between client and server
   * such as in <b-table> if sortBy is applied to the data on server side render.
   * Chrome and V8 native sorts are inconsistent/unstable
   *
   * This function uses native sort with fallback to index compare when the a and b
   * compare returns 0
   *
   * Algorithm bsaed on:
   * https://stackoverflow.com/questions/1427608/fast-stable-sorting-algorithm-implementation-in-javascript/45422645#45422645
   *
   * @param {array} array to sort
   * @param {function} sortcompare function
   * @return {array}
   */
  function stableSort(array, compareFn) {
    // Using `.bind(compareFn)` on the wrapped anonymous function improves
    // performance by avoiding the function call setup. We don't use an arrow
    // function here as it binds `this` to the `stableSort` context rather than
    // the `compareFn` context, which wouldn't give us the performance increase.
    return array.map(function (a, index) {
      return [index, a];
    }).sort(function (a, b) {
      return this(a[1], b[1]) || a[0] - b[0];
    }.bind(compareFn)).map(function (e) {
      return e[1];
    });
  }

  var IGNORED_FIELD_KEYS = {
    _rowVariant: true,
    _cellVariants: true,
    _showDetails: true // Return a copy of a row after all reserved fields have been filtered out
    // TODO: add option to specify which fields to include

  };

  function sanitizeRow(row) {
    return keys(row).reduce(function (obj, key) {
      // Ignore special fields that start with _
      if (!IGNORED_FIELD_KEYS[key]) {
        obj[key] = row[key];
      }

      return obj;
    }, {});
  } // Stringifies the values of an object
  //   { b: 3, c: { z: 'zzz', d: null, e: 2 }, d: [10, 12, 11], a: 'one' }
  // becomes
  //   'one 3 2 zzz 10 12 11'


  function toString(v) {
    if (typeof v === 'undefined' || v === null) {
      return '';
    }

    if (v instanceof Object && !(v instanceof Date)) {
      // Arrays are also object, and keys just returns the array indexes
      // Date objects we convert to strings
      return keys(v).sort()
      /* sort to prevent SSR issues on pre-rendered sorted tables */
      .map(function (k) {
        return toString(v[k]);
      }).join(' ');
    }

    return String(v);
  } // Stringifies the values of a record, ignoring any special top level field keys
  // TODO: add option to strigify formatted/scopedSlot items, and only specific fields


  function recToString(row) {
    if (!(row instanceof Object)) {
      return '';
    }

    return toString(sanitizeRow(row));
  } // Default sort compare routine
  // TODO: add option to sort by multiple columns (tri-state per column, plus order of columns in sort)
  //  where sprtBy could be an array of objects [ {key: 'foo', sortDir: 'asc'}, {key:'bar', sortDir: 'desc'} ...]
  //  or an array of arrays [ ['foo','asc'], ['bar','desc'] ]


  function defaultSortCompare(a, b, sortBy) {
    a = get(a, sortBy, '');
    b = get(b, sortBy, '');

    if (a instanceof Date && b instanceof Date || typeof a === 'number' && typeof b === 'number') {
      // Special case for comparing Dates and Numbers
      return a < b && -1 || a > b && 1 || 0;
    }

    return toString(a).localeCompare(toString(b), undefined, {
      numeric: true
    });
  } // Helper function to massage field entry into common object format


  function processField(key, value) {
    var field = null;

    if (typeof value === 'string') {
      // Label shortcut
      field = {
        key: key,
        label: value
      };
    } else if (typeof value === 'function') {
      // Formatter shortcut
      field = {
        key: key,
        formatter: value
      };
    } else if (_typeof(value) === 'object') {
      field = _objectSpread({}, value);
      field.key = field.key || key;
    } else if (value !== false) {
      // Fallback to just key
      field = {
        key: key
      };
    }

    return field;
  } // Filter CSS Selector for click/dblclick/etc events
  // If any of these selectors match the clicked element, we ignore the event


  var EVENT_FILTER = ['a', 'a *', // include content inside links
  'button', 'button *', // include content inside buttons
  'input:not(.disabled):not([disabled])', 'select:not(.disabled):not([disabled])', 'textarea:not(.disabled):not([disabled])', '[role="link"]', '[role="link"] *', '[role="button"]', '[role="button"] *', '[tabindex]:not(.disabled):not([disabled])'].join(','); // Returns true of we should ignore the click/dbclick/keypress event
  // Avoids having the user need to use @click.stop on the form control

  function filterEvent(evt) {
    if (!evt || !evt.target) {
      return;
    }

    var el = evt.target;

    if (el.tagName === 'TD' || el.tagName === 'TH' || el.tagName === 'TR' || el.disabled) {
      // Shortut all the following tests for efficiency
      return false;
    }

    if (closest('.dropdown-menu', el)) {
      // Click was in a dropdown menu, so ignore
      return true;
    }

    var label = el.tagName === 'LABEL' ? el : closest('label', el);

    if (label && label.control && !label.control.disabled) {
      // If the label's form control is not disabled then we don't propagate evt
      return true;
    }

    return matches(el, EVENT_FILTER);
  } // b-table component definition
  // @vue/component


  var BTable = {
    name: 'BTable',
    mixins: [idMixin, listenOnRootMixin],
    // Don't place ATTRS on root element automatically, as table could be wrapped in responsive div
    inheritAttrs: false,
    props: {
      items: {
        type: [Array, Function],
        default: function _default() {
          return [];
        }
      },
      fields: {
        type: [Object, Array],
        default: null
      },
      primaryKey: {
        // Primary key for record.
        // If provided the value in each row must be unique!!!
        type: String,
        default: null
      },
      sortBy: {
        type: String,
        default: null
      },
      sortDesc: {
        type: Boolean,
        default: false
      },
      sortDirection: {
        type: String,
        default: 'asc',
        validator: function validator(direction) {
          return arrayIncludes(['asc', 'desc', 'last'], direction);
        }
      },
      caption: {
        type: String,
        default: null
      },
      captionHtml: {
        type: String
      },
      captionTop: {
        type: Boolean,
        default: false
      },
      striped: {
        type: Boolean,
        default: false
      },
      bordered: {
        type: Boolean,
        default: false
      },
      borderless: {
        type: Boolean,
        default: false
      },
      outlined: {
        type: Boolean,
        default: false
      },
      dark: {
        type: Boolean,
        default: function _default() {
          /* istanbul ignore if */
          if (this && typeof this.inverse === 'boolean') {
            // Deprecate inverse
            warn("b-table: prop 'inverse' has been deprecated. Use 'dark' instead");
            return this.dark;
          }

          return false;
        }
      },
      inverse: {
        // Deprecated in v1.0.0 in favor of `dark`
        type: Boolean,
        default: null
      },
      hover: {
        type: Boolean,
        default: false
      },
      small: {
        type: Boolean,
        default: false
      },
      fixed: {
        type: Boolean,
        default: false
      },
      footClone: {
        type: Boolean,
        default: false
      },
      responsive: {
        type: [Boolean, String],
        default: false
      },
      stacked: {
        type: [Boolean, String],
        default: false
      },
      selectable: {
        type: Boolean,
        default: false
      },
      selectMode: {
        type: String,
        default: 'multi'
      },
      selectedVariant: {
        type: String,
        default: 'primary'
      },
      headVariant: {
        type: String,
        default: ''
      },
      footVariant: {
        type: String,
        default: ''
      },
      theadClass: {
        type: [String, Array],
        default: null
      },
      theadTrClass: {
        type: [String, Array],
        default: null
      },
      tbodyClass: {
        type: [String, Array],
        default: null
      },
      tbodyTrClass: {
        type: [String, Array, Function],
        default: null
      },
      tfootClass: {
        type: [String, Array],
        default: null
      },
      tfootTrClass: {
        type: [String, Array],
        default: null
      },
      perPage: {
        type: Number,
        default: 0
      },
      currentPage: {
        type: Number,
        default: 1
      },
      filter: {
        type: [String, RegExp, Object, Array, Function],
        default: null
      },
      filterFunction: {
        type: Function,
        default: null
      },
      sortCompare: {
        type: Function,
        default: null
      },
      noLocalSorting: {
        type: Boolean,
        default: false
      },
      noProviderPaging: {
        type: Boolean,
        default: false
      },
      noProviderSorting: {
        type: Boolean,
        default: false
      },
      noProviderFiltering: {
        type: Boolean,
        default: false
      },
      noSortReset: {
        type: Boolean,
        default: false
      },
      busy: {
        type: Boolean,
        default: false
      },
      value: {
        // v-model for retreiving the current displayed rows
        type: Array,
        default: function _default() {
          return [];
        }
      },
      labelSortAsc: {
        type: String,
        default: 'Click to sort Ascending'
      },
      labelSortDesc: {
        type: String,
        default: 'Click to sort Descending'
      },
      showEmpty: {
        type: Boolean,
        default: false
      },
      emptyText: {
        type: String,
        default: 'There are no records to show'
      },
      emptyHtml: {
        type: String
      },
      emptyFilteredText: {
        type: String,
        default: 'There are no records matching your request'
      },
      emptyFilteredHtml: {
        type: String
      },
      apiUrl: {
        // Passthrough prop. Passed to the context object. Not used by b-table directly
        type: String,
        default: ''
      },
      tbodyTransitionProps: {
        type: Object // default: undefined

      },
      tbodyTransitionHandlers: {
        type: Object // default: undefined

      }
    },
    data: function data() {
      return {
        localSortBy: this.sortBy || '',
        localSortDesc: this.sortDesc || false,
        localBusy: false,
        // Our local copy of the items. Must be an array
        localItems: isArray(this.items) ? this.items.slice() : [],
        // Flag for displaying which empty slot to show, and for some event triggering.
        isFiltered: false,
        selectedRows: [],
        lastRowClicked: -1
      };
    },
    computed: {
      // Layout related computed props
      isStacked: function isStacked() {
        return this.stacked === '' ? true : this.stacked;
      },
      isResponsive: function isResponsive() {
        var responsive = this.responsive === '' ? true : this.responsive;
        return this.isStacked ? false : responsive;
      },
      responsiveClass: function responsiveClass() {
        return this.isResponsive === true ? 'table-responsive' : this.isResponsive ? "table-responsive-".concat(this.responsive) : '';
      },
      tableClasses: function tableClasses() {
        var _ref;

        return _ref = {
          'table-striped': this.striped,
          'table-hover': this.hover,
          'table-dark': this.dark,
          'table-bordered': this.bordered,
          'table-borderless': this.borderless,
          'table-sm': this.small,
          border: this.outlined,
          // The following are b-table custom styles
          'b-table-fixed': this.fixed,
          'b-table-stacked': this.stacked === true || this.stacked === ''
        }, _defineProperty(_ref, "b-table-stacked-".concat(this.stacked), this.stacked !== true && this.stacked), _defineProperty(_ref, 'b-table-selectable', this.selectable), _ref;
      },
      headClasses: function headClasses() {
        return [this.headVariant ? 'thead-' + this.headVariant : '', this.theadClass];
      },
      bodyClasses: function bodyClasses() {
        return [this.tbodyClass];
      },
      footClasses: function footClasses() {
        var variant = this.footVariant || this.headVariant || null;
        return [variant ? 'thead-' + variant : '', this.tfootClass];
      },
      captionClasses: function captionClasses() {
        return {
          'b-table-caption-top': this.captionTop
        };
      },
      // Items related computed props
      hasProvider: function hasProvider() {
        return this.items instanceof Function;
      },
      localFiltering: function localFiltering() {
        return this.hasProvider ? !!this.noProviderFiltering : true;
      },
      localSorting: function localSorting() {
        return this.hasProvider ? !!this.noProviderSorting : !this.noLocalSorting;
      },
      localPaging: function localPaging() {
        return this.hasProvider ? !!this.noProviderPaging : true;
      },
      context: function context() {
        // Current state of sorting, filtering and pagination props/values
        return {
          filter: this.localFilter,
          sortBy: this.localSortBy,
          sortDesc: this.localSortDesc,
          perPage: this.perPage,
          currentPage: this.currentPage,
          apiUrl: this.apiUrl
        };
      },
      providerTriggerContext: function providerTriggerContext() {
        // Used to trigger the provider function via a watcher. Only the fields that
        // are needed for triggering a provider update are included. Note that the
        // regular this.context is sent to the provider during fetches though, as they
        // may neeed all the prop info.
        var ctx = {
          apiUrl: this.apiUrl
        };

        if (!this.noProviderFiltering) {
          // Either a string, or could be an object or array.
          ctx.filter = this.localFilter;
        }

        if (!this.noProviderSorting) {
          ctx.sortBy = this.localSortBy;
          ctx.sortDesc = this.localSortDesc;
        }

        if (!this.noProviderPaging) {
          ctx.perPage = this.perPage;
          ctx.currentPage = this.currentPage;
        }

        return ctx;
      },
      computedBusy: function computedBusy() {
        return this.busy || this.localBusy;
      },
      computedFields: function computedFields() {
        var _this = this;

        // We normalize fields into an array of objects
        // [ { key:..., label:..., ...}, {...}, ..., {..}]
        var fields = [];

        if (isArray(this.fields)) {
          // Normalize array Form
          this.fields.filter(function (f) {
            return f;
          }).forEach(function (f) {
            if (typeof f === 'string') {
              fields.push({
                key: f,
                label: toStartCaseStr(f)
              });
            } else if (_typeof(f) === 'object' && f.key && typeof f.key === 'string') {
              // Full object definition. We use assign so that we don't mutate the original
              fields.push(_objectSpread({}, f));
            } else if (_typeof(f) === 'object' && keys(f).length === 1) {
              // Shortcut object (i.e. { 'foo_bar': 'This is Foo Bar' }
              var key = keys(f)[0];
              var field = processField(key, f[key]);

              if (field) {
                fields.push(field);
              }
            }
          });
        } else if (this.fields && _typeof(this.fields) === 'object' && keys(this.fields).length > 0) {
          // Normalize object Form
          keys(this.fields).forEach(function (key) {
            var field = processField(key, _this.fields[key]);

            if (field) {
              fields.push(field);
            }
          });
        } // If no field provided, take a sample from first record (if exits)


        if (fields.length === 0 && this.localItems.length > 0) {
          var sample = this.localItems[0];
          keys(sample).forEach(function (k) {
            if (!IGNORED_FIELD_KEYS[k]) {
              fields.push({
                key: k,
                label: toStartCaseStr(k)
              });
            }
          });
        } // Ensure we have a unique array of fields and that they have String labels


        var memo = {};
        return fields.filter(function (f) {
          if (!memo[f.key]) {
            memo[f.key] = true;
            f.label = typeof f.label === 'string' ? f.label : toStartCaseStr(f.key);
            return true;
          }

          return false;
        });
      },
      filteredCheck: function filteredCheck() {
        // For watching changes to filteredItems vs localItems
        return {
          filteredItems: this.filteredItems,
          localItems: this.localItems,
          localFilter: this.localFilter
        };
      },
      localFilter: function localFilter() {
        // Returns a sanitized/normalized version of filter prop
        if (typeof this.filter === 'function') {
          // this.localFilterFn will contain the correct function ref.
          // Deprecate setting prop filter to a function
          return '';
        } else if (typeof this.filterFunction !== 'function' && !(typeof this.filter === 'string' || this.filter instanceof RegExp)) {
          // Using internal filter function, which only acccepts string or regexp at the moment
          return '';
        } else {
          // Could be astring, object or array, as needed by external filter function
          return this.filter;
        }
      },
      localFilterFn: function localFilterFn() {
        var filter = this.filter;
        var filterFn = this.filterFunction; // Sanitized/normalize filter-function prop

        if (typeof filterFn === 'function') {
          return filterFn;
        } else if (typeof filter === 'function') {
          // Deprecate setting prop filter to a function
          return filter;
        } else {
          // no filterFunction, so signal to use internal filter function
          return null;
        }
      },
      filteredItems: function filteredItems() {
        // Returns the records in localItems that match the filter criteria.
        // Returns the original localItems array if not sorting
        var items = this.localItems || [];
        var criteria = this.localFilter;
        var filterFn = this.filterFnFactory(this.localFilterFn, criteria) || this.defaultFilterFnFactory(criteria); // We only do local filtering if requested, and if the are records to filter and
        // if a filter criteria was specified

        if (this.localFiltering && filterFn && items.length > 0) {
          items = items.filter(filterFn);
        }

        return items;
      },
      sortedItems: function sortedItems() {
        // Sorts the filtered items and returns a new array of the sorted items
        // or the original items array if not sorted.
        var items = this.filteredItems || [];
        var sortBy = this.localSortBy;
        var sortDesc = this.localSortDesc;
        var sortCompare = this.sortCompare;
        var localSorting = this.localSorting;

        if (sortBy && localSorting) {
          // stableSort returns a new arary, and leaves the original array intact
          return stableSort(items, function (a, b) {
            var result = null;

            if (typeof sortCompare === 'function') {
              // Call user provided sortCompare routine
              result = sortCompare(a, b, sortBy, sortDesc);
            }

            if (result === null || result === undefined || result === false) {
              // Fallback to built-in defaultSortCompare if sortCompare not defined or returns null/false
              result = defaultSortCompare(a, b, sortBy);
            } // Negate result if sorting in descending order


            return (result || 0) * (sortDesc ? -1 : 1);
          });
        }

        return items;
      },
      paginatedItems: function paginatedItems() {
        var items = this.sortedItems || [];
        var currentPage = Math.max(parseInt(this.currentPage, 10) || 1, 1);
        var perPage = Math.max(parseInt(this.perPage, 10) || 0, 0); // Apply local pagination

        if (this.localPaging && !!perPage) {
          // Grab the current page of data (which may be past filtered items limit)
          items = items.slice((currentPage - 1) * perPage, currentPage * perPage);
        } // Return the items to display in the table


        return items;
      },
      computedItems: function computedItems() {
        return this.paginatedItems || [];
      }
    },
    watch: {
      // Watch props for changes and update local values
      items: function items(newItems) {
        if (this.hasProvider || newItems instanceof Function) {
          this.$nextTick(this._providerUpdate);
        } else if (isArray(newItems)) {
          // Set localItems/filteredItems to a copy of the provided array
          this.localItems = newItems.slice();
        } else {
          this.localItems = [];
        }
      },
      sortDesc: function sortDesc(newVal, oldVal) {
        if (newVal === this.localSortDesc) {
          return;
        }

        this.localSortDesc = newVal || false;
      },
      sortBy: function sortBy(newVal, oldVal) {
        if (newVal === this.localSortBy) {
          return;
        }

        this.localSortBy = newVal || null;
      },
      selectMode: function selectMode(newVal, oldVal) {
        if (oldVal !== newVal) {
          this.clearSelected();
        }
      },
      // Update .sync props
      localSortDesc: function localSortDesc(newVal, oldVal) {
        // Emit update to sort-desc.sync
        if (newVal !== oldVal) {
          this.clearSelected();
          this.$emit('update:sortDesc', newVal);
        }
      },
      localSortBy: function localSortBy(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.clearSelected();
          this.$emit('update:sortBy', newVal);
        }
      },
      localBusy: function localBusy(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.$emit('update:busy', newVal);
        }
      },
      // Watch for changes on computedItems and update the v-model
      computedItems: function computedItems(newVal, oldVal) {
        // Reset for selectable
        this.lastRowClicked = -1;
        this.$emit('input', newVal);
        var equal = false;

        if (this.selectable && this.selectedRows.length > 0) {
          // Quick check against array length
          equal = isArray(newVal) && isArray(oldVal) && newVal.length === oldVal.length;

          for (var i = 0; equal && i < newVal.length; i++) {
            // Look for the first non-loosely equal row, after ignoring reserved fields
            equal = looseEqual(sanitizeRow(newVal[i]), sanitizeRow(oldVal[i]));
          }
        }

        if (!equal) {
          this.clearSelected();
        }
      },
      selectable: function selectable(newVal, oldVal) {
        // Clear selection if prop selectable changes
        this.clearSelected();
      },
      // Watch for changes to the filter criteria and filtered items vs localItems).
      // And set visual state and emit events as required
      filteredCheck: function filteredCheck(_ref2) {
        var filteredItems = _ref2.filteredItems,
            localItems = _ref2.localItems,
            localFilter = _ref2.localFilter;
        // Determine if the dataset is filtered or not
        var isFiltered;

        if (!localFilter) {
          // If filter criteria is falsey
          isFiltered = false;
        } else if (looseEqual(localFilter, []) || looseEqual(localFilter, {})) {
          // If filter criteria is an empty array or object
          isFiltered = false;
        } else if (localFilter) {
          // if Filter criteria is truthy
          isFiltered = true;
        } else {
          isFiltered = false;
        }

        if (isFiltered) {
          this.clearSelected();
          this.$emit('filtered', filteredItems, filteredItems.length);
        }

        this.isFiltered = isFiltered;
      },
      isFiltered: function isFiltered(newVal, oldVal) {
        if (newVal !== oldVal) {
          this.clearSelected();
        }

        if (newVal === false && oldVal === true) {
          // We need to emit a filtered event if isFiltered transitions from true to
          // false so that users can update their pagination controls.
          this.$emit('filtered', this.localItems, this.localItems.length);
        }
      },
      context: function context(newVal, oldVal) {
        // Emit context info for enternal paging/filtering/sorting handling
        if (!looseEqual(newVal, oldVal)) {
          this.$emit('context-changed', newVal);
        }
      },
      // Provider update triggering
      providerTriggerContext: function providerTriggerContext(newVal, oldVal) {
        // Trigger the provider to update as the relevant context values have changed.
        if (!looseEqual(newVal, oldVal)) {
          this.$nextTick(this._providerUpdate);
        }
      }
    },
    mounted: function mounted() {
      var _this2 = this;

      // Call the items provider if necessary
      if (this.hasProvider && (!this.localItems || this.localItems.length === 0)) {
        // Fetch on mount if localItems is empty
        this._providerUpdate();
      } // Initially update the v-model of displayed items


      this.$emit('input', this.computedItems); // Listen for global messages to tell us to force refresh the table

      this.listenOnRoot('bv::refresh::table', function (id) {
        if (id === _this2.id || id === _this2) {
          _this2.refresh();
        }
      });
    },
    methods: {
      // Methods for computing classes, attributes and styles for table cells
      fieldClasses: function fieldClasses(field) {
        // header field (th) classes
        return [field.variant ? 'table-' + field.variant : '', field.class ? field.class : '', field.thClass ? field.thClass : ''];
      },
      tdClasses: function tdClasses(field, item) {
        var cellVariant = '';

        if (item._cellVariants && item._cellVariants[field.key]) {
          cellVariant = "".concat(this.dark ? 'bg' : 'table', "-").concat(item._cellVariants[field.key]);
        }

        return [field.variant && !cellVariant ? "".concat(this.dark ? 'bg' : 'table', "-").concat(field.variant) : '', cellVariant, field.class ? field.class : '', this.getTdValues(item, field.key, field.tdClass, '')];
      },
      tdAttrs: function tdAttrs(field, item, colIndex) {
        var attrs = {};
        attrs['aria-colindex'] = String(colIndex + 1);

        if (field.isRowHeader) {
          attrs['scope'] = 'row';
        }

        if (this.isStacked) {
          // Generate the "header cell" label content in stacked mode
          attrs['data-label'] = field.label;

          if (field.isRowHeader) {
            attrs['role'] = 'rowheader';
          } else {
            attrs['role'] = 'cell';
          }
        }

        return _objectSpread({}, attrs, this.getTdValues(item, field.key, field.tdAttr, {}));
      },
      rowClasses: function rowClasses(item) {
        return [item._rowVariant ? "".concat(this.dark ? 'bg' : 'table', "-").concat(item._rowVariant) : '', typeof this.tbodyTrClass === 'function' ? this.tbodyTrClass(item, 'row') : this.tbodyTrClass];
      },
      getTdValues: function getTdValues(item, key, tdValue, defValue) {
        var parent = this.$parent;

        if (tdValue) {
          var value = get(item, key, '');

          if (typeof tdValue === 'function') {
            return tdValue(value, key, item);
          } else if (typeof tdValue === 'string' && typeof parent[tdValue] === 'function') {
            return parent[tdValue](value, key, item);
          }

          return tdValue;
        }

        return defValue;
      },
      // Method to get the value for a field
      getFormattedValue: function getFormattedValue(item, field) {
        var key = field.key;
        var formatter = field.formatter;
        var parent = this.$parent;
        var value = get(item, key, null);

        if (formatter) {
          if (typeof formatter === 'function') {
            value = formatter(value, key, item);
          } else if (typeof formatter === 'string' && typeof parent[formatter] === 'function') {
            value = parent[formatter](value, key, item);
          }
        }

        return value === null || typeof value === 'undefined' ? '' : value;
      },
      // Filter Function factories
      filterFnFactory: function filterFnFactory(filterFn, criteria) {
        // Wrapper factory for external filter functions.
        // Wrap the provided filter-function and return a new function.
        // returns null if no filter-function defined or if criteria is falsey.
        // Rather than directly grabbing this.computedLocalFilterFn or this.filterFunction
        // We have it passed, so that the caller computed prop will be reactive to changes
        // in the original filter-function (as this routine is a method)
        if (!filterFn || !criteria || typeof filterFn !== 'function') {
          return null;
        } // Build the wrapped filter test function, passing the criteria to the provided function


        var fn = function fn(item) {
          // Generated function returns true if the crieria matches part of the serialzed data, otherwise false
          return filterFn(item, criteria);
        }; // return the wrapped function


        return fn;
      },
      defaultFilterFnFactory: function defaultFilterFnFactory(criteria) {
        // Generates the default filter function, using the given flter criteria
        if (!criteria || !(typeof criteria === 'string' || criteria instanceof RegExp)) {
          // Bult in filter can only support strings or RegExp criteria (at the moment)
          return null;
        } // Build the regexp needed for filtering


        var regexp = criteria;

        if (typeof regexp === 'string') {
          // Escape special RegExp characters in the string and convert contiguous
          // whitespace to \s+ matches
          var pattern = criteria.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&').replace(/[\s\uFEFF\xA0]+/g, '\\s+'); // Build the RegExp (no need for global flag, as we only need to find the value once in the string)

          regexp = new RegExp(".*".concat(pattern, ".*"), 'i');
        } // Generate the wrapped filter test function to use


        var fn = function fn(item) {
          // This searches all row values (and sub property values) in the entire (excluding
          // special _ prefixed keys), because we convert the record to a space-separated
          // string containing all the value properties (recursively), even ones that are
          // not visible (not specified in this.fields).
          //
          // TODO: enable searching on formatted fields and scoped slots
          // TODO: should we filter only on visible fields (i.e. ones in this.fields) by default?
          // TODO: allow for searching on specific fields/key, this could be combined with the previous TODO
          // TODO: give recToString extra options for filtering (i.e. passing the fields definition
          //      and a reference to $scopedSlots)
          //
          // Generated function returns true if the crieria matches part of the serialzed data, otherwise false
          // We set lastIndex = 0 on regex in case someone uses the /g global flag
          regexp.lastIndex = 0;
          return regexp.test(recToString(item));
        }; // Return the generated function


        return fn;
      },
      clearSelected: function clearSelected() {
        var hasSelection = this.selectedRows.reduce(function (prev, v) {
          return prev || v;
        }, false);

        if (hasSelection) {
          this.lastRowClicked = -1;
          this.selectedRows = [];
          this.$emit('row-selected', []);
        }
      },
      // Event handlers
      rowClicked: function rowClicked(e, item, index) {
        var _this3 = this;

        if (this.stopIfBusy(e)) {
          // If table is busy (via provider) then don't propagate
          return;
        } else if (filterEvent(e)) {
          // clicked on a non-disabled control so ignore
          return;
        }

        if (e.type === 'keydown') {
          // If the click was generated by space or enter, stop page scroll
          e.stopPropagation();
          e.preventDefault();
        }

        if (this.selectable) {
          var selected = !this.selectedRows[index];

          switch (this.selectMode) {
            case 'single':
              this.selectedRows = [];
              break;

            case 'range':
              if (this.lastRowClicked >= 0 && e.shiftKey) {
                // range
                for (var idx = Math.min(this.lastRowClicked, index); idx <= Math.max(this.lastRowClicked, index); idx++) {
                  this.selectedRows[idx] = true;
                }

                selected = true;
              } else {
                if (!(e.ctrlKey || e.metaKey)) {
                  // clear range selection if any
                  this.selectedRows = [];
                  selected = true;
                }

                this.lastRowClicked = selected ? index : -1;
              }

              break;
          }

          this.$set(this.selectedRows, index, selected);
          var items = [];
          this.selectedRows.forEach(function (v, idx) {
            if (v) {
              items.push(_this3.computedItems[idx]);
            }
          });
          this.$emit('row-selected', items);
        }

        this.$emit('row-clicked', item, index, e);
      },
      middleMouseRowClicked: function middleMouseRowClicked(e, item, index) {
        if (this.stopIfBusy(e)) {
          // If table is busy (via provider) then don't propagate
          return;
        }

        this.$emit('row-middle-clicked', item, index, e);
      },
      rowDblClicked: function rowDblClicked(e, item, index) {
        if (this.stopIfBusy(e)) {
          // If table is busy (via provider) then don't propagate
          return;
        } else if (filterEvent(e)) {
          // clicked on a non-disabled control so ignore
          return;
        }

        this.$emit('row-dblclicked', item, index, e);
      },
      rowHovered: function rowHovered(e, item, index) {
        if (this.stopIfBusy(e)) {
          // If table is busy (via provider) then don't propagate
          return;
        }

        this.$emit('row-hovered', item, index, e);
      },
      rowUnhovered: function rowUnhovered(e, item, index) {
        if (this.stopIfBusy(e)) {
          // If table is busy (via provider) then don't propagate
          return;
        }

        this.$emit('row-unhovered', item, index, e);
      },
      rowContextmenu: function rowContextmenu(e, item, index) {
        if (this.stopIfBusy(e)) {
          // If table is busy (via provider) then don't propagate
          return;
        }

        this.$emit('row-contextmenu', item, index, e);
      },
      headClicked: function headClicked(e, field) {
        var _this4 = this;

        if (this.stopIfBusy(e)) {
          // If table is busy (via provider) then don't propagate
          return;
        } else if (filterEvent(e)) {
          // clicked on a non-disabled control so ignore
          return;
        }

        e.stopPropagation();
        e.preventDefault();
        var sortChanged = false;

        var toggleLocalSortDesc = function toggleLocalSortDesc() {
          var sortDirection = field.sortDirection || _this4.sortDirection;

          if (sortDirection === 'asc') {
            _this4.localSortDesc = false;
          } else if (sortDirection === 'desc') {
            _this4.localSortDesc = true;
          }
        };

        if (field.sortable) {
          if (field.key === this.localSortBy) {
            // Change sorting direction on current column
            this.localSortDesc = !this.localSortDesc;
          } else {
            // Start sorting this column ascending
            this.localSortBy = field.key;
            toggleLocalSortDesc();
          }

          sortChanged = true;
        } else if (this.localSortBy && !this.noSortReset) {
          this.localSortBy = null;
          toggleLocalSortDesc();
          sortChanged = true;
        }

        this.$emit('head-clicked', field.key, field, e);

        if (sortChanged) {
          // Sorting parameters changed
          this.$emit('sort-changed', this.context);
        }
      },
      stopIfBusy: function stopIfBusy(evt) {
        if (this.computedBusy) {
          // If table is busy (via provider) then don't propagate
          evt.preventDefault();
          evt.stopPropagation();
          return true;
        }

        return false;
      },
      // Exposed method(s)
      refresh: function refresh() {
        this.$off('refreshed', this.refresh);

        if (this.computedBusy) {
          // Can't force an update when forced busy by user (busy prop === true)
          if (this.localBusy && this.hasProvider) {
            // But if provider running (localBusy), re-schedule refresh once `refreshed` emitted
            this.$on('refreshed', this.refresh);
          }
        } else {
          this.clearSelected();

          if (this.hasProvider) {
            this.$nextTick(this._providerUpdate);
          } else {
            this.localItems = isArray(this.items) ? this.items.slice() : [];
          }
        }
      },
      // Provider related methods
      _providerSetLocal: function _providerSetLocal(items) {
        this.localItems = isArray(items) ? items.slice() : [];
        this.localBusy = false;
        this.$emit('refreshed'); // New root emit

        if (this.id) {
          this.emitOnRoot('bv::table::refreshed', this.id);
        }
      },
      _providerUpdate: function _providerUpdate() {
        // Refresh the provider function items.
        if (!this.hasProvider) {
          // Do nothing if no provider
          return;
        } // If table is busy, wait until refereshed before calling again


        if (this.computedBusy) {
          // Schedule a new refresh once `refreshed` is emitted
          this.$nextTick(this.refresh);
          return;
        } // Set internal busy state


        this.localBusy = true; // Call provider function with context and optional callback after DOM is fully updated

        this.$nextTick(function () {
          var _this5 = this;

          try {
            // Call provider function passing it the context and optional callback
            var data = this.items(this.context, this._providerSetLocal);

            if (data && data.then && typeof data.then === 'function') {
              // Provider returned Promise
              data.then(function (items) {
                // Provider resolved with items
                _this5._providerSetLocal(items);
              });
            } else if (isArray(data)) {
              // Provider returned Array data
              this._providerSetLocal(data);
            } else if (this.items.length !== 2) {
              // Check number of arguments provider function requested
              // Provider not using callback (didn't request second argument), so we clear
              // busy state as most likely there was an error in the provider function
              warn("b-table provider function didn't request calback and did not return a promise or data");
              this.localBusy = false;
            }
          } catch (e)
          /* istanbul ignore next */
          {
            // Provider function borked on us, so we spew out a warning
            // and clear the busy state
            warn("b-table provider function error [".concat(e.name, "] ").concat(e.message));
            this.localBusy = false;
            this.$off('refreshed', this.refresh);
          }
        });
      }
    },
    render: function render(h) {
      var _this6 = this;

      var $slots = this.$slots;
      var $scoped = this.$scopedSlots;
      var fields = this.computedFields;
      var items = this.computedItems;
      var tableStriped = this.striped;
      var hasRowClickHandler = this.$listeners['row-clicked'] || this.selectable; // Build the caption

      var caption = h(false);
      var captionId = null;

      if (this.caption || this.captionHtml || $slots['table-caption']) {
        captionId = this.isStacked ? this.safeId('_caption_') : null;
        var data = {
          key: 'caption',
          id: captionId,
          class: this.captionClasses
        };

        if (!$slots['table-caption']) {
          data.domProps = htmlOrText(this.captionHtml, this.caption);
        }

        caption = h('caption', data, $slots['table-caption']);
      } // Build the colgroup


      var colgroup = $slots['table-colgroup'] ? h('colgroup', {
        key: 'colgroup'
      }, $slots['table-colgroup']) : h(false); // Support scoped and unscoped slots when needed

      var normalizeSlot = function normalizeSlot(slotName) {
        var slotScope = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
        var slot = $scoped[slotName] || $slots[slotName];
        return typeof slot === 'function' ? slot(slotScope) : slot;
      }; // factory function for thead and tfoot cells (th's)


      var makeHeadCells = function makeHeadCells() {
        var isFoot = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : false;
        return fields.map(function (field, colIndex) {
          var ariaLabel = '';

          if (!field.label.trim() && !field.headerTitle) {
            // In case field's label and title are empty/blank
            // We need to add a hint about what the column is about for non-dighted users
            ariaLabel = toStartCaseStr(field.key);
          }

          var ariaLabelSorting = field.sortable ? _this6.localSortDesc && _this6.localSortBy === field.key ? _this6.labelSortAsc : _this6.labelSortDesc : null; // Assemble the aria-label

          ariaLabel = [ariaLabel, ariaLabelSorting].filter(function (a) {
            return a;
          }).join(': ') || null;
          var ariaSort = field.sortable && _this6.localSortBy === field.key ? _this6.localSortDesc ? 'descending' : 'ascending' : field.sortable ? 'none' : null;
          var data = {
            key: field.key,
            class: _this6.fieldClasses(field),
            style: field.thStyle || {},
            attrs: {
              tabindex: field.sortable ? '0' : null,
              abbr: field.headerAbbr || null,
              title: field.headerTitle || null,
              scope: isFoot ? null : 'col',
              'aria-colindex': String(colIndex + 1),
              'aria-label': ariaLabel,
              'aria-sort': ariaSort
            },
            on: {
              click: function click(evt) {
                _this6.headClicked(evt, field);
              },
              keydown: function keydown(evt) {
                var keyCode = evt.keyCode;

                if (keyCode === KeyCodes.ENTER || keyCode === KeyCodes.SPACE) {
                  _this6.headClicked(evt, field);
                }
              }
            }
          };
          var slot = isFoot && $scoped["FOOT_".concat(field.key)] ? $scoped["FOOT_".concat(field.key)] : $scoped["HEAD_".concat(field.key)];

          if (slot) {
            slot = [slot({
              label: field.label,
              column: field.key,
              field: field
            })];
          } else {
            data.domProps = htmlOrText(field.labelHtml, field.label);
          }

          return h('th', data, slot);
        });
      }; // Build the thead


      var thead = h(false);

      if (this.isStacked !== true) {
        // If in always stacked mode (this.isStacked === true), then we don't bother rendering the thead
        thead = h('thead', {
          key: 'thead',
          class: this.headClasses
        }, [h('tr', {
          class: this.theadTrClass
        }, makeHeadCells(false))]);
      } // Build the tfoot


      var tfoot = h(false);

      if (this.footClone && this.isStacked !== true) {
        // If in always stacked mode (this.isStacked === true), then we don't bother rendering the tfoot
        tfoot = h('tfoot', {
          key: 'tfoot',
          class: this.footClasses
        }, [h('tr', {
          class: this.tfootTrClass
        }, makeHeadCells(true))]);
      } // Prepare the tbody rows


      var rows = []; // Add static Top Row slot (hidden in visibly stacked mode as we can't control the data-label)
      // If in always stacked mode, we don't bother rendering the row

      if ($scoped['top-row'] && this.isStacked !== true) {
        rows.push(h('tr', {
          key: 'top-row',
          staticClass: 'b-table-top-row',
          class: [typeof this.tbodyTrClass === 'function' ? this.tbodyTrClass(null, 'row-top') : this.tbodyTrClass]
        }, [$scoped['top-row']({
          columns: fields.length,
          fields: fields
        })]));
      } else {
        rows.push(h(false));
      } // Add the item data rows or the busy slot


      if ($slots['table-busy'] && this.computedBusy) {
        // Show the busy slot
        var trAttrs = {
          role: this.isStacked ? 'row' : null
        };
        var tdAttrs = {
          colspan: String(fields.length),
          role: this.isStacked ? 'cell' : null
        };
        rows.push(h('tr', {
          key: 'table-busy-slot',
          staticClass: 'b-table-busy-slot',
          class: [typeof this.tbodyTrClass === 'function' ? this.tbodyTrClass(null, 'table-busy') : this.tbodyTrClass],
          attrs: trAttrs
        }, [h('td', {
          attrs: tdAttrs
        }, [$slots['table-busy']])]));
      } else {
        // Show the rows
        items.forEach(function (item, rowIndex) {
          var detailsSlot = $scoped['row-details'];
          var rowShowDetails = Boolean(item._showDetails && detailsSlot);
          var rowSelected = _this6.selectedRows[rowIndex]; // Details ID needed for aria-describedby when details showing

          var detailsId = rowShowDetails ? _this6.safeId("_details_".concat(rowIndex, "_")) : null;

          var toggleDetailsFn = function toggleDetailsFn() {
            if (detailsSlot) {
              _this6.$set(item, '_showDetails', !item._showDetails);
            }
          }; // For each item data field in row


          var tds = fields.map(function (field, colIndex) {
            var formatted = _this6.getFormattedValue(item, field);

            var data = {
              // For the Vue key, we concatinate the column index and field key (as field keys can be duplicated)
              key: "row-".concat(rowIndex, "-cell-").concat(colIndex, "-").concat(field.key),
              class: _this6.tdClasses(field, item),
              attrs: _this6.tdAttrs(field, item, colIndex),
              domProps: {}
            };
            var childNodes;

            if ($scoped[field.key]) {
              childNodes = [$scoped[field.key]({
                item: item,
                index: rowIndex,
                field: field,
                unformatted: get(item, field.key, ''),
                value: formatted,
                toggleDetails: toggleDetailsFn,
                detailsShowing: Boolean(item._showDetails),
                rowSelected: Boolean(rowSelected)
              })];

              if (_this6.isStacked) {
                // We wrap in a DIV to ensure rendered as a single cell when visually stacked!
                childNodes = [h('div', {}, [childNodes])];
              }
            } else {
              if (_this6.isStacked) {
                // We wrap in a DIV to ensure rendered as a single cell when visually stacked!
                childNodes = [h('div', formatted)];
              } else {
                // Non stacked
                childNodes = formatted;
              }
            } // Render either a td or th cell


            return h(field.isRowHeader ? 'th' : 'td', data, childNodes);
          }); // Calculate the row number in the dataset (indexed from 1)

          var ariaRowIndex = null;

          if (_this6.currentPage && _this6.perPage && _this6.perPage > 0) {
            ariaRowIndex = String((_this6.currentPage - 1) * _this6.perPage + rowIndex + 1);
          } // Create a unique key based on the record content, to ensure that sub components are
          // re-rendered rather than re-used, which can cause issues. If a primary key is not provided
          // we concatinate the row number and stringified record (in case there are duplicate records).
          // See: https://github.com/bootstrap-vue/bootstrap-vue/issues/2410


          var rowKey = _this6.primaryKey && typeof item[_this6.primaryKey] !== 'undefined' ? toString(item[_this6.primaryKey]) : "".concat(rowIndex, "__").concat(recToString(item)); // Assemble and add the row

          rows.push(h('tr', {
            key: "__b-table-row-".concat(rowKey, "__"),
            class: [_this6.rowClasses(item), _defineProperty({
              'b-table-has-details': rowShowDetails,
              'b-row-selected': rowSelected
            }, "".concat(_this6.dark ? 'bg' : 'table', "-").concat(_this6.selectedVariant), rowSelected && _this6.selectedVariant)],
            attrs: {
              tabindex: hasRowClickHandler ? '0' : null,
              'aria-describedby': detailsId,
              'aria-owns': detailsId,
              'aria-rowindex': ariaRowIndex,
              'aria-selected': _this6.selectable ? rowSelected ? 'true' : 'false' : null,
              role: _this6.isStacked ? 'row' : null
            },
            on: {
              // TODO: only instatiate handlers if we have registered listeners
              auxclick: function auxclick(evt) {
                if (evt.which === 2) {
                  _this6.middleMouseRowClicked(evt, item, rowIndex);
                }
              },
              click: function click(evt) {
                _this6.rowClicked(evt, item, rowIndex);
              },
              keydown: function keydown(evt) {
                var keyCode = evt.keyCode;

                if (keyCode === KeyCodes.ENTER || keyCode === KeyCodes.SPACE) {
                  if (evt.target && evt.target.tagName === 'TR' && evt.target === document.activeElement) {
                    _this6.rowClicked(evt, item, rowIndex);
                  }
                }
              },
              contextmenu: function contextmenu(evt) {
                _this6.rowContextmenu(evt, item, rowIndex);
              },
              // Note: these events are not accessibility friendly
              dblclick: function dblclick(evt) {
                _this6.rowDblClicked(evt, item, rowIndex);
              },
              mouseenter: function mouseenter(evt) {
                _this6.rowHovered(evt, item, rowIndex);
              },
              mouseleave: function mouseleave(evt) {
                _this6.rowUnhovered(evt, item, rowIndex);
              }
            }
          }, tds)); // Row Details slot

          if (rowShowDetails) {
            var _tdAttrs = {
              colspan: String(fields.length)
            };
            var _trAttrs = {
              id: detailsId
            };

            if (_this6.isStacked) {
              _tdAttrs['role'] = 'cell';
              _trAttrs['role'] = 'row';
            }

            var details = h('td', {
              attrs: _tdAttrs
            }, [detailsSlot({
              item: item,
              index: rowIndex,
              fields: fields,
              toggleDetails: toggleDetailsFn
            })]);

            if (tableStriped) {
              // Add a hidden row to keep table row striping consistent when details showing
              rows.push(h('tr', {
                key: "__b-table-details-".concat(rowIndex, "-stripe__"),
                staticClass: 'd-none',
                attrs: {
                  'aria-hidden': 'true'
                }
              }));
            }

            rows.push(h('tr', {
              key: "__b-table-details-".concat(rowIndex, "__"),
              staticClass: 'b-table-details',
              class: [typeof _this6.tbodyTrClass === 'function' ? _this6.tbodyTrClass(item, 'row-details') : _this6.tbodyTrClass],
              attrs: _trAttrs
            }, [details]));
          } else if (detailsSlot) {
            // Only add the placeholder if a the table has a row-details slot defined (but not shown)
            rows.push(h(false));

            if (tableStriped) {
              // add extra placeholder if table is striped
              rows.push(h(false));
            }
          }
        });
      } // Empty Items / Empty Filtered Row slot


      if (this.showEmpty && (!items || items.length === 0) && !($slots['table-busy'] && this.computedBusy)) {
        var empty = normalizeSlot(this.isFiltered ? 'emptyfiltered' : 'empty', {
          emptyFilteredHtml: this.emptyFilteredHtml,
          emptyFilteredText: this.emptyFilteredText,
          emptyHtml: this.emptyHtml,
          emptyText: this.emptyText,
          fields: fields,
          items: items
        });

        if (!empty) {
          empty = h('div', {
            class: ['text-center', 'my-2'],
            domProps: this.isFiltered ? htmlOrText(this.emptyFilteredHtml, this.emptyFilteredText) : htmlOrText(this.emptyHtml, this.emptyText)
          });
        }

        empty = h('td', {
          attrs: {
            colspan: String(fields.length),
            role: this.isStacked ? 'cell' : null
          }
        }, [h('div', {
          attrs: {
            role: 'alert',
            'aria-live': 'polite'
          }
        }, [empty])]);
        rows.push(h('tr', {
          key: '__b-table-empty-row__',
          staticClass: 'b-table-empty-row',
          class: [typeof this.tbodyTrClass === 'function' ? this.tbodyTrClass(null, 'row-empty') : this.tbodyTrClass],
          attrs: this.isStacked ? {
            role: 'row'
          } : {}
        }, [empty]));
      } else {
        rows.push(h(false));
      } // Static bottom row slot (hidden in visibly stacked mode as we can't control the data-label)
      // If in always stacked mode, we don't bother rendering the row


      if ($scoped['bottom-row'] && this.isStacked !== true) {
        rows.push(h('tr', {
          key: '__b-table-bottom-row__',
          staticClass: 'b-table-bottom-row',
          class: [typeof this.tbodyTrClass === 'function' ? this.tbodyTrClass(null, 'row-bottom') : this.tbodyTrClass]
        }, [$scoped['bottom-row']({
          columns: fields.length,
          fields: fields
        })]));
      } else {
        rows.push(h(false));
      } // Is tbody transition enabled


      var isTransGroup = this.tbodyTransitionProps || this.tbodyTransitionHandlers;
      var tbodyProps = {};
      var tbodyOn = {};

      if (isTransGroup) {
        tbodyOn = this.tbodyTransitionHandlers || {};
        tbodyProps = _objectSpread({}, this.tbodyTransitionProps || {}, {
          tag: 'tbody'
        });
      } // Assemble the rows into the tbody


      var tbody = h(isTransGroup ? 'transition-group' : 'tbody', {
        props: tbodyProps,
        on: tbodyOn,
        class: this.bodyClasses,
        attrs: this.isStacked ? {
          role: 'rowgroup'
        } : {}
      }, rows); // Assemble table

      var table = h('table', {
        key: 'b-table',
        staticClass: 'table b-table',
        class: this.tableClasses,
        attrs: _objectSpread({
          // We set aria-rowcount before merging in $attrs, in case user has supplied their own
          'aria-rowcount': this.filteredItems.length > items.length ? String(this.filteredItems.length) : null
        }, this.$attrs, {
          // Now we can override any $attrs here
          id: this.safeId(),
          role: this.isStacked ? 'table' : null,
          'aria-multiselectable': this.selectable ? this.selectMode === 'single' ? 'false' : 'true' : null,
          'aria-busy': this.computedBusy ? 'true' : 'false',
          'aria-colcount': String(fields.length),
          'aria-describedby': [// Preserve user supplied aria-describedby, if provided in $attrs
          (this.$attrs || {})['aria-describedby'], captionId].filter(function (a) {
            return a;
          }).join(' ') || null
        })
      }, [caption, colgroup, thead, tfoot, tbody]); // Add responsive wrapper if needed and return table

      return this.isResponsive ? h('div', {
        key: 'b-table-responsive',
        class: this.responsiveClass
      }, [table]) : table;
    }
  };

  var components$y = {
    BTable: BTable
  };
  var index$v = {
    install: function install(Vue) {
      registerComponents(Vue, components$y);
    }
  };

  var BTabButtonHelper = {
    name: 'BTabButtonHelper',
    props: {
      // Reference to the child b-tab instance
      tab: {
        default: null,
        required: true
      },
      id: {
        type: String,
        default: null
      },
      controls: {
        type: String,
        default: null
      },
      tabIndex: {
        type: Number,
        default: null
      },
      posInSet: {
        type: Number,
        default: null
      },
      setSize: {
        type: Number,
        default: null
      },
      noKeyNav: {
        type: Boolean,
        default: false
      }
    },
    methods: {
      focus: function focus() {
        if (this.$refs && this.$refs.link && this.$refs.link.focus) {
          this.$refs.link.focus();
        }
      },
      handleEvt: function handleEvt(evt) {
        function stop() {
          evt.preventDefault();
          evt.stopPropagation();
        }

        if (this.tab.disabled) {
          return;
        }

        var type = evt.type;
        var key = evt.keyCode;
        var shift = evt.shiftKey;

        if (type === 'click') {
          stop();
          this.$emit('click', evt); // Could call this.tab.activate() instead
        } else if (type === 'keydown' && !this.noKeyNav && key === KeyCodes.SPACE) {
          // In keyNav mode, SAPCE press will also trigger a click/select
          stop();
          this.$emit('click', evt); // Could call this.tab.activate() instead
        } else if (type === 'keydown' && !this.noKeyNav) {
          // For keyboard navigation
          if (key === KeyCodes.UP || key === KeyCodes.LEFT || key === KeyCodes.HOME) {
            stop();

            if (shift || key === KeyCodes.HOME) {
              this.$emit('first', evt);
            } else {
              this.$emit('prev', evt);
            }
          } else if (key === KeyCodes.DOWN || key === KeyCodes.RIGHT || key === KeyCodes.END) {
            stop();

            if (shift || key === KeyCodes.END) {
              this.$emit('last', evt);
            } else {
              this.$emit('next', evt);
            }
          }
        }
      }
    },
    render: function render(h) {
      var link = h(BLink, {
        ref: 'link',
        staticClass: 'nav-link',
        class: [{
          active: this.tab.localActive && !this.tab.disabled,
          disabled: this.tab.disabled
        }, this.tab.titleLinkClass],
        props: {
          href: this.tab.href,
          // To be deprecated to always be '#'
          disabled: this.tab.disabled
        },
        attrs: {
          role: 'tab',
          id: this.id,
          // Roving tab index when keynav enabled
          tabindex: this.tabIndex,
          'aria-selected': this.tab.localActive && !this.tab.disabled ? 'true' : 'false',
          'aria-setsize': this.setSize,
          'aria-posinset': this.posInSet,
          'aria-controls': this.controls
        },
        on: {
          click: this.handleEvt,
          keydown: this.handleEvt
        }
      }, [this.tab.$slots.title || this.tab.title]);
      return h('li', {
        staticClass: 'nav-item',
        class: [this.tab.titleItemClass],
        attrs: {
          role: 'presentation'
        }
      }, [link]);
    }
  }; // Filter function to filter out disabled tabs

  function notDisabled(tab) {
    return !tab.disabled;
  } // @vue/component


  var BTabs = {
    name: 'BTabs',
    mixins: [idMixin],
    provide: function provide() {
      return {
        bTabs: this
      };
    },
    props: {
      tag: {
        type: String,
        default: 'div'
      },
      card: {
        type: Boolean,
        default: false
      },
      small: {
        type: Boolean,
        default: false
      },
      pills: {
        type: Boolean,
        default: false
      },
      vertical: {
        type: Boolean,
        default: false
      },
      bottom: {
        type: Boolean,
        default: false
      },
      end: {
        // Synonym for 'bottom'
        type: Boolean,
        default: false
      },
      noFade: {
        type: Boolean,
        default: false
      },
      noNavStyle: {
        type: Boolean,
        default: false
      },
      noKeyNav: {
        type: Boolean,
        default: false
      },
      lazy: {
        // This prop is sniffed by the tab child
        type: Boolean,
        default: false
      },
      contentClass: {
        type: [String, Array, Object],
        default: null
      },
      navClass: {
        type: [String, Array, Object],
        default: null
      },
      navWrapperClass: {
        type: [String, Array, Object],
        default: null
      },
      value: {
        // v-model
        type: Number,
        default: null
      }
    },
    data: function data() {
      return {
        // Index of current tab
        currentTab: parseInt(this.value, 10) || -1,
        // Array of direct child b-tab instances
        tabs: []
      };
    },
    computed: {
      fade: function fade() {
        // This computed prop is sniffed by the tab child
        return !this.noFade;
      },
      navStyle: function navStyle() {
        return this.pills ? 'pills' : 'tabs';
      }
    },
    watch: {
      currentTab: function currentTab(val, old) {
        var index = -1; // Ensure only one tab is active at most

        this.tabs.forEach(function (tab, idx) {
          if (val === idx && !tab.disabled) {
            tab.localActive = true;
            index = idx;
          } else {
            tab.localActive = false;
          }
        }); // update the v-model

        this.$emit('input', index);
      },
      value: function value(val, old) {
        if (val !== old) {
          val = parseInt(val, 10);
          old = parseInt(old, 10) || 0;
          var tabs = this.tabs;

          if (tabs[val] && !tabs[val].disabled) {
            this.currentTab = val;
          } else {
            // Try next or prev tabs
            if (val < old) {
              this.previousTab();
            } else {
              this.nextTab();
            }
          }
        }
      }
    },
    created: function created() {
      // For SSR and to make sure only a single tab is shown on mount
      this.updateTabs();
    },
    mounted: function mounted() {
      // In case tabs have changed before mount
      this.updateTabs(); // Observe Child changes so we can update list of tabs

      observeDOM(this.$refs.tabsContainer, this.updateTabs.bind(this), {
        subtree: false
      });
    },
    methods: {
      // Update list of b-tab children
      updateTabs: function updateTabs() {
        // Probe tabs
        var tabs = (this.$slots.default || []).map(function (vnode) {
          return vnode.componentInstance;
        }).filter(function (tab) {
          return tab && tab._isTab;
        }); // Find *last* active non-disabled tab in current tabs
        // We trust tab state over currentTab, in case tabs were added/removed/re-ordered

        var tabIndex = tabs.indexOf(tabs.slice().reverse().find(function (tab) {
          return tab.localActive && !tab.disabled;
        })); // Else try setting to currentTab

        if (tabIndex < 0) {
          var currentTab = this.currentTab;

          if (currentTab >= tabs.length) {
            // Handle last tab being removed, so find the last non-disabled tab
            tabIndex = tabs.indexOf(tabs.slice().reverse().find(notDisabled));
          } else if (tabs[currentTab] && !tabs[currentTab].disabled) {
            // current tab is not disabled
            tabIndex = currentTab;
          }
        } // Else find *first* non-disabled tab in current tabs


        if (tabIndex < 0) {
          tabIndex = tabs.indexOf(tabs.find(notDisabled));
        } // Set the current tab state to active


        tabs.forEach(function (tab, idx) {
          tab.localActive = idx === tabIndex && !tab.disabled;
        }); // Update the array of tab children

        this.tabs = tabs; // Set the currentTab index (can be -1 if no non-disabled tabs)

        this.currentTab = tabIndex;
      },
      // Find a button taht controls a tab, given the tab reference
      // Returns the button vm instance
      getButtonForTab: function getButtonForTab(tab) {
        return (this.$refs.buttons || []).find(function (btn) {
          return btn.tab === tab;
        });
      },
      // Force a button to re-render it's content, given a b-tab instance
      // Called by b-tab on update()
      updateButton: function updateButton(tab) {
        var button = this.getButtonForTab(tab);

        if (button && button.$forceUpdate) {
          button.$forceUpdate();
        }
      },
      // Activate a tab given a b-tab instance
      // Also accessed by b-tab
      activateTab: function activateTab(tab) {
        var result = false;

        if (tab) {
          var index = this.tabs.indexOf(tab);

          if (!tab.disabled && index > -1) {
            result = true;
            this.currentTab = index;
          }
        }

        this.$emit('input', this.currentTab);
        return result;
      },
      // Deactivate a tab given a b-tab instance
      // Accessed by b-tab
      deactivateTab: function deactivateTab(tab) {
        if (tab) {
          // Find first non-disabled tab that isn't the one being deactivated
          // If no available tabs, then don't deactivate current tab
          return this.activateTab(this.tabs.filter(function (t) {
            return t !== tab;
          }).find(notDisabled));
        } else {
          // No tab specified
          return false;
        }
      },
      // Focus a tab button given it's b-tab instance
      focusButton: function focusButton(tab) {
        var _this = this;

        // Wrap in nextTick to ensure DOM has completed rendering/updating before focusing
        this.$nextTick(function () {
          var button = _this.getButtonForTab(tab);

          if (button && button.focus) {
            button.focus();
          }
        });
      },
      // Emit a click event on a specified b-tab component instance
      emitTabClick: function emitTabClick(tab, evt) {
        if (evt && evt instanceof Event && tab && tab.$emit && !tab.disabled) {
          tab.$emit('click', evt);
        }
      },
      // Click Handler
      clickTab: function clickTab(tab, evt) {
        this.activateTab(tab);
        this.emitTabClick(tab, evt);
      },
      // Move to first non-disabled tab
      firstTab: function firstTab(focus) {
        var tab = this.tabs.find(notDisabled);

        if (this.activateTab(tab) && focus) {
          this.focusButton(tab);
          this.emitTabClick(tab, focus);
        }
      },
      // Move to previous non-disabled tab
      previousTab: function previousTab(focus) {
        var currentIndex = Math.max(this.currentTab, 0);
        var tab = this.tabs.slice(0, currentIndex).reverse().find(notDisabled);

        if (this.activateTab(tab) && focus) {
          this.focusButton(tab);
          this.emitTabClick(tab, focus);
        }
      },
      // Move to next non-disabled tab
      nextTab: function nextTab(focus) {
        var currentIndex = Math.max(this.currentTab, -1);
        var tab = this.tabs.slice(currentIndex + 1).find(notDisabled);

        if (this.activateTab(tab) && focus) {
          this.focusButton(tab);
          this.emitTabClick(tab, focus);
        }
      },
      // Move to last non-disabled tab
      lastTab: function lastTab(focus) {
        var tab = this.tabs.slice().reverse().find(notDisabled);

        if (this.activateTab(tab) && focus) {
          this.focusButton(tab);
          this.emitTabClick(tab, focus);
        }
      }
    },
    render: function render(h) {
      var _this2 = this,
          _ref;

      var tabs = this.tabs; // Currently active tab

      var activeTab = tabs.find(function (tab) {
        return tab.localActive && !tab.disabled;
      }); // Tab button to allow focusing when no actgive tab found (keynav only)

      var fallbackTab = tabs.find(function (tab) {
        return !tab.disabled;
      }); // For each b-tab found create the tab buttons

      var buttons = tabs.map(function (tab, index) {
        var buttonId = tab.controlledBy || _this2.safeId("_BV_tab_".concat(index + 1, "_"));

        var tabIndex = null; // Ensure at least one tab button is focusable when keynav enabled (if possible)

        if (!_this2.noKeyNav) {
          // Buttons are not in tab index unless active, or a fallback tab
          tabIndex = -1;

          if (activeTab === tab || !activeTab && fallbackTab === tab) {
            // Place tab button in tab sequence
            tabIndex = null;
          }
        }

        return h(BTabButtonHelper, {
          key: tab._uid || buttonId || index,
          ref: 'buttons',
          // Needed to make this.$refs.buttons an array
          refInFor: true,
          props: {
            tab: tab,
            id: buttonId,
            controls: _this2.safeId('_BV_tab_container_'),
            tabIndex: tabIndex,
            setSize: tabs.length,
            posInSet: index + 1,
            noKeyNav: _this2.noKeyNav
          },
          on: {
            click: function click(evt) {
              _this2.clickTab(tab, evt);
            },
            first: _this2.firstTab,
            prev: _this2.previousTab,
            next: _this2.nextTab,
            last: _this2.lastTab
          }
        });
      }); // Nav 'button' wrapper

      var navs = h('ul', {
        class: ['nav', (_ref = {}, _defineProperty(_ref, "nav-".concat(this.navStyle), !this.noNavStyle), _defineProperty(_ref, "card-header-".concat(this.navStyle), this.card && !this.vertical), _defineProperty(_ref, 'card-header', this.card && this.vertical), _defineProperty(_ref, 'h-100', this.card && this.vertical), _defineProperty(_ref, 'flex-column', this.vertical), _defineProperty(_ref, 'border-bottom-0', this.vertical), _defineProperty(_ref, 'rounded-0', this.vertical), _defineProperty(_ref, "small", this.small), _ref), this.navClass],
        attrs: {
          role: 'tablist',
          id: this.safeId('_BV_tab_controls_')
        }
      }, [buttons, this.$slots.tabs]);
      navs = h('div', {
        class: [{
          'card-header': this.card && !this.vertical && !(this.end || this.bottom),
          'card-footer': this.card && !this.vertical && (this.end || this.bottom),
          'col-auto': this.vertical
        }, this.navWrapperClass]
      }, [navs]);
      var empty;

      if (tabs && tabs.length) {
        empty = h(false);
      } else {
        empty = h('div', {
          key: 'empty-tab',
          class: ['tab-pane', 'active', {
            'card-body': this.card
          }]
        }, this.$slots.empty);
      } // Main content section


      var content = h('div', {
        ref: 'tabsContainer',
        staticClass: 'tab-content',
        class: [{
          col: this.vertical
        }, this.contentClass],
        attrs: {
          id: this.safeId('_BV_tab_container_')
        }
      }, [this.$slots.default, empty]); // Render final output

      return h(this.tag, {
        staticClass: 'tabs',
        class: {
          row: this.vertical,
          'no-gutters': this.vertical && this.card
        },
        attrs: {
          id: this.safeId()
        }
      }, [this.end || this.bottom ? content : h(false), [navs], this.end || this.bottom ? h(false) : content]);
    }
  };

  var BTab = {
    name: 'BTab',
    mixins: [idMixin],
    inject: {
      bTabs: {
        default: function _default() {
          return {
            // Dont set a tab index if not rendered inside b-tabs
            noKeyNav: true
          };
        }
      }
    },
    props: {
      active: {
        type: Boolean,
        default: false
      },
      tag: {
        type: String,
        default: 'div'
      },
      buttonId: {
        type: String,
        default: ''
      },
      title: {
        type: String,
        default: ''
      },
      titleItemClass: {
        // Sniffed by tabs.js and added to nav 'li.nav-item'
        type: [String, Array, Object],
        default: null
      },
      titleLinkClass: {
        // Sniffed by tabs.js and added to nav 'a.nav-link'
        type: [String, Array, Object],
        default: null
      },
      headHtml: {
        // Is this actually ever used?
        type: String,
        default: null
      },
      disabled: {
        type: Boolean,
        default: false
      },
      noBody: {
        type: Boolean,
        default: false
      },
      href: {
        // This should be deprecated, as tabs are not navigation (URL) based
        // <b-nav> + <b-card> + <router-view>/<nuxt-child> should be used instead
        // And we dont support router-links here
        type: String,
        default: '#'
      },
      lazy: {
        type: Boolean,
        default: false
      }
    },
    data: function data() {
      return {
        localActive: this.active && !this.disabled,
        show: false
      };
    },
    computed: {
      tabClasses: function tabClasses() {
        return [this.bTabs.card && !this.noBody ? 'card-body' : '', this.show ? 'show' : '', this.computedFade ? 'fade' : '', this.disabled ? 'disabled' : '', this.localActive ? 'active' : ''];
      },
      controlledBy: function controlledBy() {
        return this.buttonId || this.safeId('__BV_tab_button__');
      },
      computedFade: function computedFade() {
        return this.bTabs.fade || false;
      },
      computedLazy: function computedLazy() {
        return this.bTabs.lazy || this.lazy;
      },
      _isTab: function _isTab() {
        // For parent sniffing of child
        return true;
      }
    },
    watch: {
      localActive: function localActive(newVal, oldVal) {
        // Make 'active' prop work with `.sync` modifier
        this.$emit('update:active', newVal);
      },
      active: function active(newVal, oldVal) {
        if (newVal !== oldVal) {
          if (newVal) {
            // If activated post mount
            this.activate();
          } else {
            if (!this.deactivate()) {
              // Tab couldn't be deactivated, so we reset the synced active prop
              // Deactivation will fail if no other tabs to activate.
              this.$emit('update:active', this.localActive);
            }
          }
        }
      },
      disabled: function disabled(newVal, oldVal) {
        if (newVal !== oldVal) {
          if (newVal && this.localActive && this.bTabs.firstTab) {
            this.localActive = false;
            this.bTabs.firstTab();
          }
        }
      }
    },
    mounted: function mounted() {
      // Initially show on mount if active and not disabled
      this.show = this.localActive;
    },
    updated: function updated() {
      // Force the tab button content to update (since slots are not reactive)
      // Only done if we have a title slot, as the title prop is reactive
      if (this.$slots.title && this.bTabs.updateButton) {
        this.bTabs.updateButton(this);
      }
    },
    methods: {
      // Transition handlers
      beforeEnter: function beforeEnter()
      /* instanbul ignore next: difficult to test rAF in JSDOM */
      {
        var _this = this;

        // change opacity (add 'show' class) 1 frame after display
        // otherwise css transition won't happen
        // TODO: Move raf method into utils/dom.js
        var raf = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.msRequestAnimationFrame || window.oRequestAnimationFrame ||
        /* istanbul ignore next */
        function (cb) {
          setTimeout(cb, 16);
        };

        raf(function () {
          _this.show = true;
        });
      },
      beforeLeave: function beforeLeave()
      /* instanbul ignore next: difficult to test rAF in JSDOM */
      {
        // Remove the 'show' class
        this.show = false;
      },
      // Public methods
      activate: function activate() {
        if (this.bTabs.activateTab && !this.disabled) {
          return this.bTabs.activateTab(this);
        } else {
          // Not inside a b-tabs component or tab is disabled
          return false;
        }
      },
      deactivate: function deactivate() {
        if (this.bTabs.deactivateTab && this.localActive) {
          return this.bTabs.deactivateTab(this);
        } else {
          // Not inside a b-tabs component or not active to begin with
          return false;
        }
      }
    },
    render: function render(h) {
      var content = h(this.tag, {
        ref: 'panel',
        staticClass: 'tab-pane',
        class: this.tabClasses,
        directives: [{
          name: 'show',
          value: this.localActive
        }],
        attrs: {
          role: 'tabpanel',
          id: this.safeId(),
          tabindex: this.localActive && !this.bTabs.noKeyNav ? '0' : null,
          'aria-hidden': this.localActive ? 'false' : 'true',
          'aria-expanded': this.localActive ? 'true' : 'false',
          'aria-labelledby': this.controlledBy || null
        }
      }, // Render content lazily if requested
      [this.localActive || !this.computedLazy ? this.$slots.default : h(false)]);
      return h('transition', {
        props: {
          mode: 'out-in'
        },
        on: {
          beforeEnter: this.beforeEnter,
          beforeLeave: this.beforeLeave
        }
      }, [content]);
    }
  };

  var components$z = {
    BTabs: BTabs,
    BTab: BTab
  };
  var index$w = {
    install: function install(Vue) {
      registerComponents(Vue, components$z);
    }
  };

  var BTooltip = {
    name: 'BTooltip',
    mixins: [toolpopMixin],
    props: {
      title: {
        type: String,
        default: ''
      },
      triggers: {
        type: [String, Array],
        default: 'hover focus'
      },
      placement: {
        type: String,
        default: 'top'
      }
    },
    data: function data() {
      return {};
    },
    methods: {
      createToolpop: function createToolpop() {
        // getTarget is in toolpop mixin
        var target = this.getTarget();

        if (target) {
          this._toolpop = new ToolTip(target, this.getConfig(), this.$root);
        } else {
          this._toolpop = null;
          warn("b-tooltip: 'target' element not found!");
        }

        return this._toolpop;
      }
    },
    render: function render(h) {
      return h('div', {
        class: ['d-none'],
        style: {
          display: 'none'
        },
        attrs: {
          'aria-hidden': true
        }
      }, [h('div', {
        ref: 'title'
      }, this.$slots.default)]);
    }
  };

  var inBrowser$3 = typeof window !== 'undefined' && typeof document !== 'undefined'; // Key which we use to store tooltip object on element

  var BVTT = '__BV_ToolTip__'; // Valid event triggers

  var validTriggers$1 = {
    focus: true,
    hover: true,
    click: true,
    blur: true // Build a ToolTip config based on bindings (if any)
    // Arguments and modifiers take precedence over passed value config object

    /* istanbul ignore next: not easy to test */

  };

  function parseBindings$1(bindings) {
    // We start out with a blank config
    var config = {}; // Process bindings.value

    if (typeof bindings.value === 'string') {
      // Value is tooltip content (html optionally supported)
      config.title = bindings.value;
    } else if (typeof bindings.value === 'function') {
      // Title generator function
      config.title = bindings.value;
    } else if (_typeof(bindings.value) === 'object') {
      // Value is config object, so merge
      config = _objectSpread({}, config, bindings.value);
    } // If Argument, assume element ID of container element


    if (bindings.arg) {
      // Element ID specified as arg. We must prepend '#' to become a CSS selector
      config.container = "#".concat(bindings.arg);
    } // Process modifiers


    keys(bindings.modifiers).forEach(function (mod) {
      if (/^html$/.test(mod)) {
        // Title allows HTML
        config.html = true;
      } else if (/^nofade$/.test(mod)) {
        // no animation
        config.animation = false;
      } else if (/^(auto|top(left|right)?|bottom(left|right)?|left(top|bottom)?|right(top|bottom)?)$/.test(mod)) {
        // placement of tooltip
        config.placement = mod;
      } else if (/^(window|viewport)$/.test(mod)) {
        // bounday of tooltip
        config.boundary = mod;
      } else if (/^d\d+$/.test(mod)) {
        // delay value
        var delay = parseInt(mod.slice(1), 10) || 0;

        if (delay) {
          config.delay = delay;
        }
      } else if (/^o-?\d+$/.test(mod)) {
        // offset value. Negative allowed
        var offset = parseInt(mod.slice(1), 10) || 0;

        if (offset) {
          config.offset = offset;
        }
      }
    }); // Special handling of event trigger modifiers Trigger is a space separated list

    var selectedTriggers = {}; // parse current config object trigger

    var triggers = typeof config.trigger === 'string' ? config.trigger.trim().split(/\s+/) : [];
    triggers.forEach(function (trigger) {
      if (validTriggers$1[trigger]) {
        selectedTriggers[trigger] = true;
      }
    }); // Parse Modifiers for triggers

    keys(validTriggers$1).forEach(function (trigger) {
      if (bindings.modifiers[trigger]) {
        selectedTriggers[trigger] = true;
      }
    }); // Sanitize triggers

    config.trigger = keys(selectedTriggers).join(' ');

    if (config.trigger === 'blur') {
      // Blur by itself is useless, so convert it to 'focus'
      config.trigger = 'focus';
    }

    if (!config.trigger) {
      // remove trigger config
      delete config.trigger;
    }

    return config;
  } //
  // Add or Update tooltip on our element
  //

  /* istanbul ignore next: not easy to test */


  function applyBVTT(el, bindings, vnode) {
    if (!inBrowser$3) {
      return;
    }

    if (!Popper) {
      // Popper is required for tooltips to work
      warn('v-b-tooltip: Popper.js is required for tooltips to work');
      return;
    }

    if (el[BVTT]) {
      el[BVTT].updateConfig(parseBindings$1(bindings));
    } else {
      el[BVTT] = new ToolTip(el, parseBindings$1(bindings), vnode.context.$root);
    }
  } //
  // Remove tooltip on our element
  //

  /* istanbul ignore next: not easy to test */


  function removeBVTT(el) {
    if (!inBrowser$3) {
      return;
    }

    if (el[BVTT]) {
      el[BVTT].destroy();
      el[BVTT] = null;
      delete el[BVTT];
    }
  }
  /*
   * Export our directive
   */

  /* istanbul ignore next: not easy to test */


  var bTooltip = {
    bind: function bind(el, bindings, vnode) {
      applyBVTT(el, bindings, vnode);
    },
    inserted: function inserted(el, bindings, vnode) {
      applyBVTT(el, bindings, vnode);
    },
    update: function update(el, bindings, vnode) {
      if (bindings.value !== bindings.oldValue) {
        applyBVTT(el, bindings, vnode);
      }
    },
    componentUpdated: function componentUpdated(el, bindings, vnode) {
      if (bindings.value !== bindings.oldValue) {
        applyBVTT(el, bindings, vnode);
      }
    },
    unbind: function unbind(el) {
      removeBVTT(el);
    }
  };

  var directives$3 = {
    bTooltip: bTooltip
  };
  var tooltipDirectivePlugin = {
    install: function install(Vue) {
      registerDirectives(Vue, directives$3);
    }
  };

  var components$A = {
    BTooltip: BTooltip
  };
  var index$x = {
    install: function install(Vue) {
      registerComponents(Vue, components$A);
      Vue.use(tooltipDirectivePlugin);
    }
  };



  var componentPlugins = /*#__PURE__*/Object.freeze({
    Alert: index,
    Badge: index$1,
    Breadcrumb: index$2,
    Button: index$3,
    ButtonToolbar: index$5,
    ButtonGroup: index$4,
    Card: index$7,
    Carousel: index$8,
    Collapse: collapsePlugin,
    Dropdown: dropdownPlugin,
    Embed: index$a,
    Form: index$b,
    FormGroup: index$c,
    FormInput: index$f,
    FormTextarea: index$g,
    FormFile: index$h,
    FormCheckbox: index$d,
    FormRadio: index$e,
    FormSelect: index$i,
    Image: index$j,
    InputGroup: index$6,
    Jumbotron: index$k,
    Layout: index$9,
    Link: index$l,
    ListGroup: index$m,
    Media: index$n,
    Modal: index$o,
    Nav: navPlugin,
    Navbar: index$p,
    Pagination: index$q,
    PaginationNav: index$r,
    Popover: index$s,
    Progress: index$t,
    Spinner: index$u,
    Table: index$v,
    Tabs: index$w,
    Tooltip: index$x
  });

  /*
   * Constants / Defaults
   */

  var NAME$2 = 'v-b-scrollspy';
  var ACTIVATE_EVENT = 'bv::scrollspy::activate';
  var Default = {
    element: 'body',
    offset: 10,
    method: 'auto',
    throttle: 75
  };
  var DefaultType = {
    element: '(string|element|component)',
    offset: 'number',
    method: 'string',
    throttle: 'number'
  };
  var ClassName$2 = {
    DROPDOWN_ITEM: 'dropdown-item',
    ACTIVE: 'active'
  };
  var Selector$4 = {
    ACTIVE: '.active',
    NAV_LIST_GROUP: '.nav, .list-group',
    NAV_LINKS: '.nav-link',
    NAV_ITEMS: '.nav-item',
    LIST_ITEMS: '.list-group-item',
    DROPDOWN: '.dropdown, .dropup',
    DROPDOWN_ITEMS: '.dropdown-item',
    DROPDOWN_TOGGLE: '.dropdown-toggle'
  };
  var OffsetMethod = {
    OFFSET: 'offset',
    POSITION: 'position' // HREFs must start with # but can be === '#', or start with '#/' or '#!' (which can be router links)

  };
  var HREF_REGEX = /^#[^/!]+/; // Transition Events

  var TransitionEndEvents$2 = ['webkitTransitionEnd', 'transitionend', 'otransitionend', 'oTransitionEnd']; // Options for events

  var EventOptions$3 = {
    passive: true,
    capture: false
    /*
     * Utility Methods
     */
    // Better var type detection

  };

  function toType(obj)
  /* istanbul ignore next: not easy to test */
  {
    return {}.toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase();
  } // Check config properties for expected types


  function typeCheckConfig(componentName, config, configTypes)
  /* istanbul ignore next: not easy to test */
  {
    for (var property in configTypes) {
      if (Object.prototype.hasOwnProperty.call(configTypes, property)) {
        var expectedTypes = configTypes[property];
        var value = config[property];
        var valueType = value && isElement(value) ? 'element' : toType(value); // handle Vue instances

        valueType = value && value._isVue ? 'component' : valueType;

        if (!new RegExp(expectedTypes).test(valueType)) {
          warn("".concat(componentName, ": Option \"").concat(property, "\" provided type \"").concat(valueType, "\" but expected type \"").concat(expectedTypes, "\""));
        }
      }
    }
  }
  /*
   * ------------------------------------------------------------------------
   * Class Definition
   * ------------------------------------------------------------------------
   */

  /* istanbul ignore next: not easy to test */


  var ScrollSpy
  /* istanbul ignore next: not easy to test */
  =
  /*#__PURE__*/
  function () {
    function ScrollSpy(element, config, $root) {
      _classCallCheck(this, ScrollSpy);

      // The element we activate links in
      this.$el = element;
      this.$scroller = null;
      this.$selector = [Selector$4.NAV_LINKS, Selector$4.LIST_ITEMS, Selector$4.DROPDOWN_ITEMS].join(',');
      this.$offsets = [];
      this.$targets = [];
      this.$activeTarget = null;
      this.$scrollHeight = 0;
      this.$resizeTimeout = null;
      this.$obs_scroller = null;
      this.$obs_targets = null;
      this.$root = $root || null;
      this.$config = null;
      this.updateConfig(config);
    }

    _createClass(ScrollSpy, [{
      key: "updateConfig",
      value: function updateConfig(config, $root) {
        if (this.$scroller) {
          // Just in case out scroll element has changed
          this.unlisten();
          this.$scroller = null;
        }

        var cfg = _objectSpread({}, this.constructor.Default, config);

        if ($root) {
          this.$root = $root;
        }

        typeCheckConfig(this.constructor.Name, cfg, this.constructor.DefaultType);
        this.$config = cfg;

        if (this.$root) {
          var self = this;
          this.$root.$nextTick(function () {
            self.listen();
          });
        } else {
          this.listen();
        }
      }
    }, {
      key: "dispose",
      value: function dispose() {
        this.unlisten();
        clearTimeout(this.$resizeTimeout);
        this.$resizeTimeout = null;
        this.$el = null;
        this.$config = null;
        this.$scroller = null;
        this.$selector = null;
        this.$offsets = null;
        this.$targets = null;
        this.$activeTarget = null;
        this.$scrollHeight = null;
      }
    }, {
      key: "listen",
      value: function listen() {
        var _this = this;

        var scroller = this.getScroller();

        if (scroller && scroller.tagName !== 'BODY') {
          eventOn(scroller, 'scroll', this, EventOptions$3);
        }

        eventOn(window, 'scroll', this, EventOptions$3);
        eventOn(window, 'resize', this, EventOptions$3);
        eventOn(window, 'orientationchange', this, EventOptions$3);
        TransitionEndEvents$2.forEach(function (evtName) {
          eventOn(window, evtName, _this, EventOptions$3);
        });
        this.setObservers(true); // Scedule a refresh

        this.handleEvent('refresh');
      }
    }, {
      key: "unlisten",
      value: function unlisten() {
        var _this2 = this;

        var scroller = this.getScroller();
        this.setObservers(false);

        if (scroller && scroller.tagName !== 'BODY') {
          eventOff(scroller, 'scroll', this, EventOptions$3);
        }

        eventOff(window, 'scroll', this, EventOptions$3);
        eventOff(window, 'resize', this, EventOptions$3);
        eventOff(window, 'orientationchange', this, EventOptions$3);
        TransitionEndEvents$2.forEach(function (evtName) {
          eventOff(window, evtName, _this2, EventOptions$3);
        });
      }
    }, {
      key: "setObservers",
      value: function setObservers(on) {
        var _this3 = this;

        // We observe both the scroller for content changes, and the target links
        if (this.$obs_scroller) {
          this.$obs_scroller.disconnect();
          this.$obs_scroller = null;
        }

        if (this.$obs_targets) {
          this.$obs_targets.disconnect();
          this.$obs_targets = null;
        }

        if (on) {
          this.$obs_targets = observeDOM(this.$el, function () {
            _this3.handleEvent('mutation');
          }, {
            subtree: true,
            childList: true,
            attributes: true,
            attributeFilter: ['href']
          });
          this.$obs_scroller = observeDOM(this.getScroller(), function () {
            _this3.handleEvent('mutation');
          }, {
            subtree: true,
            childList: true,
            characterData: true,
            attributes: true,
            attributeFilter: ['id', 'style', 'class']
          });
        }
      } // general event handler

    }, {
      key: "handleEvent",
      value: function handleEvent(evt) {
        var type = typeof evt === 'string' ? evt : evt.type;
        var self = this;

        function resizeThrottle() {
          if (!self.$resizeTimeout) {
            self.$resizeTimeout = setTimeout(function () {
              self.refresh();
              self.process();
              self.$resizeTimeout = null;
            }, self.$config.throttle);
          }
        }

        if (type === 'scroll') {
          if (!this.$obs_scroller) {
            // Just in case we are added to the DOM before the scroll target is
            // We re-instantiate our listeners, just in case
            this.listen();
          }

          this.process();
        } else if (/(resize|orientationchange|mutation|refresh)/.test(type)) {
          // Postpone these events by throttle time
          resizeThrottle();
        }
      } // Refresh the list of target links on the element we are applied to

    }, {
      key: "refresh",
      value: function refresh() {
        var _this4 = this;

        var scroller = this.getScroller();

        if (!scroller) {
          return;
        }

        var autoMethod = scroller !== scroller.window ? OffsetMethod.POSITION : OffsetMethod.OFFSET;
        var method = this.$config.method === 'auto' ? autoMethod : this.$config.method;
        var methodFn = method === OffsetMethod.POSITION ? position : offset;
        var offsetBase = method === OffsetMethod.POSITION ? this.getScrollTop() : 0;
        this.$offsets = [];
        this.$targets = [];
        this.$scrollHeight = this.getScrollHeight(); // Find all the unique link href's

        selectAll(this.$selector, this.$el).map(function (link) {
          return getAttr(link, 'href');
        }).filter(function (href) {
          return HREF_REGEX.test(href || '');
        }).map(function (href) {
          var el = select(href, scroller);

          if (isVisible(el)) {
            return {
              offset: parseInt(methodFn(el).top, 10) + offsetBase,
              target: href
            };
          }

          return null;
        }).filter(function (item) {
          return item;
        }).sort(function (a, b) {
          return a.offset - b.offset;
        }).reduce(function (memo, item) {
          // record only unique targets/offfsets
          if (!memo[item.target]) {
            _this4.$offsets.push(item.offset);

            _this4.$targets.push(item.target);

            memo[item.target] = true;
          }

          return memo;
        }, {});
        return this;
      } // Handle activating/clearing

    }, {
      key: "process",
      value: function process() {
        var scrollTop = this.getScrollTop() + this.$config.offset;
        var scrollHeight = this.getScrollHeight();
        var maxScroll = this.$config.offset + scrollHeight - this.getOffsetHeight();

        if (this.$scrollHeight !== scrollHeight) {
          this.refresh();
        }

        if (scrollTop >= maxScroll) {
          var target = this.$targets[this.$targets.length - 1];

          if (this.$activeTarget !== target) {
            this.activate(target);
          }

          return;
        }

        if (this.$activeTarget && scrollTop < this.$offsets[0] && this.$offsets[0] > 0) {
          this.$activeTarget = null;
          this.clear();
          return;
        }

        for (var i = this.$offsets.length; i--;) {
          var isActiveTarget = this.$activeTarget !== this.$targets[i] && scrollTop >= this.$offsets[i] && (typeof this.$offsets[i + 1] === 'undefined' || scrollTop < this.$offsets[i + 1]);

          if (isActiveTarget) {
            this.activate(this.$targets[i]);
          }
        }
      }
    }, {
      key: "getScroller",
      value: function getScroller() {
        if (this.$scroller) {
          return this.$scroller;
        }

        var scroller = this.$config.element;

        if (!scroller) {
          return null;
        } else if (isElement(scroller.$el)) {
          scroller = scroller.$el;
        } else if (typeof scroller === 'string') {
          scroller = select(scroller);
        }

        if (!scroller) {
          return null;
        }

        this.$scroller = scroller.tagName === 'BODY' ? window : scroller;
        return this.$scroller;
      }
    }, {
      key: "getScrollTop",
      value: function getScrollTop() {
        var scroller = this.getScroller();
        return scroller === window ? scroller.pageYOffset : scroller.scrollTop;
      }
    }, {
      key: "getScrollHeight",
      value: function getScrollHeight() {
        return this.getScroller().scrollHeight || Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
      }
    }, {
      key: "getOffsetHeight",
      value: function getOffsetHeight() {
        var scroller = this.getScroller();
        return scroller === window ? window.innerHeight : getBCR(scroller).height;
      }
    }, {
      key: "activate",
      value: function activate(target) {
        var _this5 = this;

        this.$activeTarget = target;
        this.clear(); // Grab the list of target links (<a href="{$target}">)

        var links = selectAll(this.$selector.split(',').map(function (selector) {
          return "".concat(selector, "[href=\"").concat(target, "\"]");
        }).join(','), this.$el);
        links.forEach(function (link) {
          if (hasClass(link, ClassName$2.DROPDOWN_ITEM)) {
            // This is a dropdown item, so find the .dropdown-toggle and set it's state
            var dropdown = closest(Selector$4.DROPDOWN, link);

            if (dropdown) {
              _this5.setActiveState(select(Selector$4.DROPDOWN_TOGGLE, dropdown), true);
            } // Also set this link's state


            _this5.setActiveState(link, true);
          } else {
            // Set triggered link as active
            _this5.setActiveState(link, true);

            if (matches(link.parentElement, Selector$4.NAV_ITEMS)) {
              // Handle nav-link inside nav-item, and set nav-item active
              _this5.setActiveState(link.parentElement, true);
            } // Set triggered links parents as active
            // With both <ul> and <nav> markup a parent is the previous sibling of any nav ancestor


            var el = link;

            while (el) {
              el = closest(Selector$4.NAV_LIST_GROUP, el);
              var sibling = el ? el.previousElementSibling : null;

              if (matches(sibling, "".concat(Selector$4.NAV_LINKS, ", ").concat(Selector$4.LIST_ITEMS))) {
                _this5.setActiveState(sibling, true);
              } // Handle special case where nav-link is inside a nav-item


              if (matches(sibling, Selector$4.NAV_ITEMS)) {
                _this5.setActiveState(select(Selector$4.NAV_LINKS, sibling), true); // Add active state to nav-item as well


                _this5.setActiveState(sibling, true);
              }
            }
          }
        }); // Signal event to via $root, passing ID of activaed target and reference to array of links

        if (links && links.length > 0 && this.$root) {
          this.$root.$emit(ACTIVATE_EVENT, target, links);
        }
      }
    }, {
      key: "clear",
      value: function clear() {
        var _this6 = this;

        selectAll("".concat(this.$selector, ", ").concat(Selector$4.NAV_ITEMS), this.$el).filter(function (el) {
          return hasClass(el, ClassName$2.ACTIVE);
        }).forEach(function (el) {
          return _this6.setActiveState(el, false);
        });
      }
    }, {
      key: "setActiveState",
      value: function setActiveState(el, active) {
        if (!el) {
          return;
        }

        if (active) {
          addClass(el, ClassName$2.ACTIVE);
        } else {
          removeClass(el, ClassName$2.ACTIVE);
        }
      }
    }], [{
      key: "Name",
      get: function get() {
        return NAME$2;
      }
    }, {
      key: "Default",
      get: function get() {
        return Default;
      }
    }, {
      key: "DefaultType",
      get: function get() {
        return DefaultType;
      }
    }]);

    return ScrollSpy;
  }();

  var BVSS = '__BV_ScrollSpy__'; // Generate config from bindings

  function makeConfig(binding)
  /* istanbul ignore next: not easy to test */
  {
    var config = {}; // If Argument, assume element ID

    if (binding.arg) {
      // Element ID specified as arg. We must pre-pend #
      config.element = '#' + binding.arg;
    } // Process modifiers


    keys(binding.modifiers).forEach(function (mod) {
      if (/^\d+$/.test(mod)) {
        // Offest value
        config.offset = parseInt(mod, 10);
      } else if (/^(auto|position|offset)$/.test(mod)) {
        // Offset method
        config.method = mod;
      }
    }); // Process value

    if (typeof binding.value === 'string') {
      // Value is a CSS ID or selector
      config.element = binding.value;
    } else if (typeof binding.value === 'number') {
      // Value is offset
      config.offset = Math.round(binding.value);
    } else if (_typeof(binding.value) === 'object') {
      // Value is config object
      // Filter the object based on our supported config options
      keys(binding.value).filter(function (k) {
        return Boolean(ScrollSpy.DefaultType[k]);
      }).forEach(function (k) {
        config[k] = binding.value[k];
      });
    }

    return config;
  }

  function addBVSS(el, binding, vnode)
  /* istanbul ignore next: not easy to test */
  {
    if (isServer) {
      return;
    }

    var cfg = makeConfig(binding);

    if (!el[BVSS]) {
      el[BVSS] = new ScrollSpy(el, cfg, vnode.context.$root);
    } else {
      el[BVSS].updateConfig(cfg, vnode.context.$root);
    }

    return el[BVSS];
  }

  function removeBVSS(el)
  /* istanbul ignore next: not easy to test */
  {
    if (el[BVSS]) {
      el[BVSS].dispose();
      el[BVSS] = null;
    }
  }
  /*
   * Export our directive
   */


  var bScrollspy = {
    bind: function bind(el, binding, vnode)
    /* istanbul ignore next: not easy to test */
    {
      addBVSS(el, binding, vnode);
    },
    inserted: function inserted(el, binding, vnode)
    /* istanbul ignore next: not easy to test */
    {
      addBVSS(el, binding, vnode);
    },
    update: function update(el, binding, vnode)
    /* istanbul ignore next: not easy to test */
    {
      addBVSS(el, binding, vnode);
    },
    componentUpdated: function componentUpdated(el, binding, vnode)
    /* istanbul ignore next: not easy to test */
    {
      addBVSS(el, binding, vnode);
    },
    unbind: function unbind(el)
    /* istanbul ignore next: not easy to test */
    {
      if (isServer) {
        return;
      } // Remove scroll event listener on scrollElId


      removeBVSS(el);
    }
  };

  var directives$4 = {
    bScrollspy: bScrollspy
  };
  var index$y = {
    install: function install(Vue) {
      registerDirectives(Vue, directives$4);
    }
  };



  var directivePlugins = /*#__PURE__*/Object.freeze({
    Toggle: toggleDirectivePlugin,
    Modal: modalDirectivePlugin,
    Scrollspy: index$y,
    Tooltip: tooltipDirectivePlugin,
    Popover: popoverDirectivePlugin
  });

  var VuePlugin = {
    install: function install(Vue) {
      if (Vue._bootstrap_vue_installed) {
        return;
      }

      Vue._bootstrap_vue_installed = true; // Register component plugins

      for (var plugin in componentPlugins) {
        Vue.use(componentPlugins[plugin]);
      } // Register directive plugins


      for (var _plugin in directivePlugins) {
        Vue.use(directivePlugins[_plugin]);
      }
    }
  };
  vueUse(VuePlugin);

  return VuePlugin;

}));
//# sourceMappingURL=bootstrap-vue.js.map