/**
 * Component Registry for managing application components
 * Provides lifecycle management and dependency injection
 */

export class ComponentRegistry {
    constructor() {
        this.components = new Map();
        this.instances = new Map();
    }

    /**
     * Register a component class
     */
    register(name, ComponentClass) {
        this.components.set(name, ComponentClass);
    }

    /**
     * Create component instance
     */
    create(name, container, options = {}) {
        const ComponentClass = this.components.get(name);
        
        if (!ComponentClass) {
            throw new Error(`Component "${name}" not found`);
        }

        // Create instance with dependency injection
        const instance = new ComponentClass(container, options);
        
        // Store instance for lifecycle management
        const instanceId = this.generateInstanceId(name);
        this.instances.set(instanceId, {
            name,
            instance,
            container,
            options
        });

        // Initialize if method exists
        if (typeof instance.init === 'function') {
            instance.init();
        }

        return instance;
    }

    /**
     * Get component instance by container element
     */
    getInstance(container) {
        for (const [id, data] of this.instances) {
            if (data.container === container) {
                return data.instance;
            }
        }
        return null;
    }

    /**
     * Initialize all components found in the DOM
     */
    initializeAll() {
        this.components.forEach((ComponentClass, name) => {
            const selector = `[data-component="${name}"]`;
            const elements = document.querySelectorAll(selector);
            
            elements.forEach(element => {
                // Skip if already initialized
                if (element.hasAttribute('data-component-initialized')) {
                    return;
                }

                // Extract options from data attributes
                const options = this.extractDataAttributes(element);
                
                try {
                    this.create(name, element, options);
                    element.setAttribute('data-component-initialized', 'true');
                } catch (error) {
                    console.error(`Failed to initialize component "${name}":`, error);
                }
            });
        });
    }

    /**
     * Destroy component instance
     */
    destroy(instance) {
        for (const [id, data] of this.instances) {
            if (data.instance === instance) {
                // Call destroy method if exists
                if (typeof instance.destroy === 'function') {
                    instance.destroy();
                }
                
                // Remove from registry
                this.instances.delete(id);
                
                // Mark container as uninitialized
                if (data.container) {
                    data.container.removeAttribute('data-component-initialized');
                }
                
                break;
            }
        }
    }

    /**
     * Destroy all component instances
     */
    destroyAll() {
        this.instances.forEach((data, id) => {
            this.destroy(data.instance);
        });
    }

    /**
     * Extract data attributes as component options
     */
    extractDataAttributes(element) {
        const options = {};
        const dataset = element.dataset;
        
        Object.keys(dataset).forEach(key => {
            if (key.startsWith('option')) {
                const optionName = key.replace('option', '').toLowerCase();
                let value = dataset[key];
                
                // Try to parse as JSON for complex values
                try {
                    value = JSON.parse(value);
                } catch (e) {
                    // Keep as string if not valid JSON
                }
                
                options[optionName] = value;
            }
        });
        
        return options;
    }

    /**
     * Generate unique instance ID
     */
    generateInstanceId(componentName) {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substr(2, 9);
        return `${componentName}_${timestamp}_${random}`;
    }

    /**
     * Get all registered component names
     */
    getRegisteredComponents() {
        return Array.from(this.components.keys());
    }

    /**
     * Get all active instances
     */
    getActiveInstances() {
        return Array.from(this.instances.values());
    }
}