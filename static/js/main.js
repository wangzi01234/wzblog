// main.js 重构版本（采用模块化设计模式）
(() => {
  // ==================== 核心控制器基类 ====================
  class BaseController {
    constructor() {
      if (new.target === BaseController) {
        throw new Error('BaseController cannot be instantiated directly');
      }
      this.init();
    }

    init() {
      throw new Error('init() must be implemented by subclass');
    }
  }

  // ==================== 导航控制器 ====================
  class NavController extends BaseController {
    init() {
      this.navToggle = document.querySelector('.nav-toggle');
      this.navMenu = document.querySelector('.nav-menu');
      this.isActive = false;

      this.bindEvents();
    }

    bindEvents() {
      // 导航切换
      this.navToggle.addEventListener('click', e => this.handleToggle(e));
      
      // 全局点击关闭
      document.addEventListener('click', e => this.handleDocumentClick(e));
    }

    handleToggle(e) {
      e.stopPropagation();
      this.isActive = !this.navMenu.classList.contains('active');
      this.navMenu.classList.toggle('active', this.isActive);
    }

    handleDocumentClick(e) {
      if (!this.navMenu.contains(e.target) && 
          !this.navToggle.contains(e.target)) {
        this.navMenu.classList.remove('active');
        this.isActive = false;
      }
    }
  }

  // ==================== 筛选控制器 ====================
class FilterController extends BaseController {
  init() {
    this.filterButton = document.querySelector('.filter-button');
    this.filterDropdown = document.querySelector('.filter-dropdown');
    this.isOpen = false;
    this.setupEventListeners();
  }

  setupEventListeners() {
    this.filterButton.addEventListener('click', e => this.toggleDropdown(e));
    document.addEventListener('click', e => this.handleOutsideClick(e));
    window.addEventListener('resize', () => this.handleResponsive());
  }

  toggleDropdown(e) {
    e.stopPropagation();
    this.isOpen ? this.closeDropdown() : this.openDropdown();
  }

  handleOutsideClick(e) {
    if (
      !this.filterDropdown.contains(e.target) &&
      !this.filterButton.contains(e.target)
    ) {
      this.closeDropdown();
    }
  }

  handleResponsive() {
    if (window.innerWidth < 768 && this.isOpen) {
      this.closeDropdown();
    }
  }

  // 打开下拉面板
  openDropdown() {
    this.filterDropdown.classList.add('active');
    this.isOpen = true;
  }

  // 关闭下拉面板
  closeDropdown() {
    this.filterDropdown.classList.remove('active');
    this.isOpen = false;
  }
}

  // ==================== 初始化执行 ====================
  const initializeControllers = () => {
    try {
      new NavController();
      new FilterController();
    } catch (error) {
      console.error('Controller initialization failed:', error);
    }
  };

  // 执行初始化（DOMContentLoaded 由 defer 保证）
  initializeControllers();
})();
