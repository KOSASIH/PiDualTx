import { mount } from '@vue/test-utils';
import AutonomousDualTx from '@/components/AutonomousDualTx.vue';

describe('AutonomousDualTx.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(AutonomousDualTx);
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('renders headline with correct text and elegant style', () => {
    const headline = wrapper.find('h2');
    expect(headline.exists()).toBe(true);
    expect(headline.text()).toMatch(/Autonomous Dual Transaction/i);
    // Check for bold font weight between 600-800 and large font size (threshold approximate)
    const fontWeight = parseInt(window.getComputedStyle(headline.element).fontWeight, 10);
    expect(fontWeight).toBeGreaterThanOrEqual(600);
    expect(fontWeight).toBeLessThanOrEqual(800);
    const fontSize = parseFloat(window.getComputedStyle(headline.element).fontSize);
    expect(fontSize).toBeGreaterThanOrEqual(48);
  });

  it('has a section container with white background, rounded corners and subtle shadow', () => {
    const container = wrapper.find('section');
    expect(container.exists()).toBe(true);

    const style = window.getComputedStyle(container.element);
    expect(style.backgroundColor).toMatch(/rgba?\(255,\s*255,\s*255(?:,\s*\d?\.?\d+)?\)/); // white
    expect(style.borderRadius).toMatch(/0\.75rem|12px/);
    expect(parseFloat(style.boxShadow.split(',')[0])).not.toBeNaN(); // Existence of box shadow
  });

  it('renders a form with accessible input fields using floating labels', () => {
    const form = wrapper.find('form');
    expect(form.exists()).toBe(true);

    const input = wrapper.find('input#address');
    expect(input.exists()).toBe(true);
    expect(input.attributes('type')).toBe('text');

    const label = wrapper.find('label[for="address"]');
    expect(label.exists()).toBe(true);
    expect(label.text().toLowerCase()).toContain('stellar wallet address');
  });

  it('updates model when input changes (Stellar wallet address)', async () => {
    const input = wrapper.find('input#address');
    await input.setValue('GBRPYHIL2CI3TBTU3XK4Z6CMYJZI2KPZROHLMZYNHB7KLIH5CTFTDH6A');
    expect(wrapper.vm.form.address).toBe('GBRPYHIL2CI3TBTU3XK4Z6CMYJZI2KPZROHLMZYNHB7KLIH5CTFTDH6A');
  });

  it('submits form and shows confirmation alert with Stellar address', async () => {
    window.alert = jest.fn();

    const input = wrapper.find('input#address');
    await input.setValue('GBRPYHIL2CI3TBTU3XK4Z6CMYJZI2KPZROHLMZYNHB7KLIH5CTFTDH6A');

    await wrapper.find('form').trigger('submit.prevent');

    expect(window.alert).toHaveBeenCalledWith(
      expect.stringContaining('Transaction submitted for GBRPYHIL2CI3TBTU3XK4Z6CMYJZI2KPZROHLMZYNHB7KLIH5CTFTDH6A')
    );
  });

  it('prevents submission with invalid Stellar address (empty input)', async () => {
    window.alert = jest.fn();

    await wrapper.find('form').trigger('submit.prevent');

    // Assuming component performs validation and does not proceed with empty address
    expect(window.alert).not.toHaveBeenCalled();
  });

  it('applies consistent neutral gray color to descriptive text', () => {
    const desc = wrapper.find('p');
    expect(desc.exists()).toBe(true);
    const style = window.getComputedStyle(desc.element);
    expect(style.color).toBe('rgb(107, 114, 128)'); // #6b7280 in rgb
    expect(parseFloat(style.fontSize)).toBeGreaterThanOrEqual(16);
    expect(parseFloat(style.fontSize)).toBeLessThanOrEqual(18);
  });

  it('submit button displays correct text and has hover scale effect class', () => {
    const btn = wrapper.find('button[type="submit"]');
    expect(btn.exists()).toBe(true);
    expect(btn.text().toLowerCase()).toMatch(/submit|send|confirm/);

    // Check for classes that imply transform scale on hover (e.g. hover:scale-105)
    const classList = btn.classes();
    const hasHoverScale = classList.some(c => c.includes('hover:scale'));
    expect(hasHoverScale).toBe(true);
  });
});
