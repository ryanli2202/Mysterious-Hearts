# Authored workplace room data shared by registry and actions.
STAGES = {
    'photographer': {'shift':('studio__photo_studio',),'development':('studio__review_room',)},
    'model': {'shift':('studio__photo_studio','studio__dressing_fitting_room'),'development':('studio__review_room',)},
    'librarian': {'shift':('library__lobby_desk','library__stacks','library__reading_room','library__reservable_study_room'),'development':('library__staff_catalogue_office',)},
    'oculus': {'shift':('site_07__reception_public_displays',),'development':('site_07__public_service_supervisor_room',)},
    'cinema': {'shift':('cinema__ticket_foyer',),'development':('cinema__staff_office',)},
    'barista': {
        'shift': ('cafe__counter_seating_room', 'cafe__staff_kitchen'),
        'development': ('cafe__staff_office',),
    },
    'florist': {'shift':('flowers__shop_floor','flowers__arrangement_workroom','flowers__stockroom'),'development':('flowers__arrangement_workroom',)},
    'chef': {'shift':('noodle_shop__kitchen','noodle_shop__service_counter_view'),'development':('noodle_shop__staff_office_store',)},
    'retail': {'shift':('shopping_mall__jobseek_tenant_shop_floor','shopping_mall__tenant_receiving_room'),'development':('shopping_mall__tenant_staff_office',)},
    'arcade': {'shift':('arcade__counter_room','arcade__cabinet_floor','arcade__staff_repair_room'),'development':('arcade__staff_office',)},
    'gardener': {'shift':('public_park__garden_paths',),'development':('public_park_pavilion__supervisor_office',)},
    'bartender': {'shift':('bar__bar_seating_room','bar__service_room'),'development':('bar__staff_office',)},
}

STAFF_ROOMS={
 'studio':('photo_studio','dressing_fitting_room','recording_booth','choreography_room','review_room'),
 'library':('desk_corridor','staff_catalogue_office'),
 'site_07':('public_service_supervisor_room',),
 'cinema':('staff_corridor','projection_room','staff_office'),
 'flowers':('arrangement_workroom','stockroom'),
 'noodle_shop':('kitchen','staff_office_store'),
 'shopping_mall':('tenant_receiving_room','tenant_staff_office','tenant_store'),
 'arcade':('service_corridor','staff_repair_room','staff_office'),
 'public_park_pavilion':('tool_store','supervisor_office'),
 'bar':('service_room','staff_office'),
 'marios_pizza':('staff_kitchen_store',),'boutique':('staff_store',),
 'archive':('conservation_workshop','restricted_storage'),
 'makerspace':('tool_store',),'cycle_shop':('repair_room','parts_store'),
 'planetarium':('staff_corridor','preparation_room'),
 'sailing_club':('equipment_store',),'market':('staff_kitchen_store',),
 'nightclub':('staff_corridor','service_room'),
 'hill_tea_room':('staff_kitchen',),'farm_shop':('staff_store',),
 'pottery_studio':('kiln_room',),'marine_centre':('staff_service_room',),
 'harbour_market':('vendor_storage',),'southbank_diner':('staff_kitchen',),
}
CAST_ROOMS={
 'rei':('studio__photo_studio','studio__dressing_fitting_room'),
 'ivan':('studio__recording_booth','studio__choreography_room','studio__review_room'),
 'emily':('flowers__arrangement_workroom','flowers__stockroom'),
 'garrett':('noodle_shop__kitchen','noodle_shop__staff_office_store'),
 'lena':('archive__conservation_workshop','archive__restricted_storage'),
 'naomi':('cycle_shop__repair_room','cycle_shop__parts_store'),
 'celeste':('planetarium__staff_corridor','planetarium__preparation_room'),
 'dev':('makerspace__tool_store',), 'rosa':('market__staff_kitchen_store',),
 'daniel':('cinema__staff_corridor','cinema__projection_room','cinema__staff_office'),
 'alyssa':('archive__conservation_workshop',),
 'elias':('studio__photo_studio','studio__review_room'),
}

