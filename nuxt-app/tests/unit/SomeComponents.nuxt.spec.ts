import { it, expect } from 'vitest'
import Logo from '../../components/Logo.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'

it('can mount some component', async () => {
    const component = await mountSuspended(Logo)
    expect(component.text()).toMatchInlineSnapshot(
        '"This is an auto-imported component"'
    )
})

