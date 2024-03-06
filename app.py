from calculator import get_average_dmg_for_weapon_profile, Rerolls
from simulate import get_average_simulated_dmg_for_weapon_profile
import tkinter as tk
from tkinter import ttk

# Global window size variables
height = 100
width = 100

rerolls = ["None", "Single", "Ones", "Full"]

reroll_lookup = {
    "None": Rerolls.NONE,
    "Single": Rerolls.SINGLE,
    "Ones": Rerolls.ONES,
    "Full": Rerolls.FULL,
}


def resize_hander(event, root):
    wscale = float(event.width) / root.winfo_reqwidth()
    hscale = float(event.height) / root.winfo_reqheight()
    width = event.width
    height = event.height
    root.config(width=width, height=height)
    # root.scale("all", 0, 0, wscale, hscale)
    # root.geometry(f"{width}x{height}")


def clean_dice_intputs(dice_str):
    dice_str = dice_str.replace(" ", "")
    split = dice_str.split("+")
    if len(split) < 2:
        if "d" in split[0]:
            dice = split[0]
            val = 0
        else:
            dice = None
            val = split[0]
    else:
        dice = split[0]
        val = split[1]
    return dice, int(val)


def clamp_value_to_dice_range(val):
    return max(2, min(6, val))


def on_simulate_button():
    attacks_dice, attacks_val = clean_dice_intputs(attacks_entry.get())
    dmg_dice, dmg_val = clean_dice_intputs(weapon_dmg_entry.get())
    sustained_dice, sustained_val = clean_dice_intputs(sustained_hits_entry.get())

    if balistic_or_weapon_skill_entry.get() == "":
        balistic_skill = None
    else:
        balistic_skill = clamp_value_to_dice_range(
            int(balistic_or_weapon_skill_entry.get())
        )
    attack_str = int(attack_str_entry.get())
    target_toughness = int(toughness_entry.get())
    AP = abs(int(weapon_AP_entry.get()))
    save = int(save_entry.get())
    enemy_wounds = int(wound_per_model_entry.get())
    wound_mod = int(wound_mod_entry.get())
    hit_mod = int(hit_mod_entry.get())

    if invuln_save_entry.get() != "":
        target_invuln = int(invuln_save_entry.get())
    else:
        target_invuln = 10

    save_mod = int(save_mod_entry.get())

    if FNP_entry.get() == "":
        FNP = None
    else:
        FNP = clamp_value_to_dice_range(int(FNP_entry.get()))

    crit_hit = clamp_value_to_dice_range(int(crit_hits_entry.get()))
    crit_wound = clamp_value_to_dice_range(int(crit_wound_entry.get()))

    hits, wounds, not_saved, dmg, models = get_average_simulated_dmg_for_weapon_profile(
        int(number_of_sims.get()),
        attacks_val,
        balistic_skill,
        attack_str,
        target_toughness,
        dmg_val,
        AP,
        save,
        enemy_wounds,
        wound_rerolls=reroll_lookup[wound_rerolls.get()],
        wound_modifer=wound_mod,
        hit_rerolls=reroll_lookup[hit_rerolls.get()],
        hit_modifier=hit_mod,
        target_invuln=target_invuln,
        save_modifier=save_mod,
        save_rerolls=reroll_lookup[save_rerolls.get()],
        has_cover=var_cover.get(),
        target_FNP=FNP,
        sustained_hits=sustained_val,
        has_lethal_hits=var_lethal_hits.get(),
        has_dev_wounds=var_dev_wounds.get(),
        crit_hit_on=crit_hit,
        crit_wound_on=crit_wound,
        dmg_dice=dmg_dice,
        attacks_dice=attacks_dice,
        sustained_hits_dice=sustained_dice,
    )

    output_text.delete(1.0, tk.END)  # Clear previous output
    output_text.insert(tk.END, f"Average Hits: {hits:.2f}\n")
    output_text.insert(tk.END, f"Average Wounds: {wounds:.2f}\n")
    output_text.insert(tk.END, f"Average Unsaved: {not_saved:.2f}\n")
    output_text.insert(tk.END, f"Average Damage: {dmg:.2f}\n")
    output_text.insert(tk.END, f"Average Models Killed: {models:.2f}\n")


def on_confirm_button():
    attacks_dice, attacks_val = clean_dice_intputs(attacks_entry.get())
    dmg_dice, dmg_val = clean_dice_intputs(weapon_dmg_entry.get())
    sustained_dice, sustained_val = clean_dice_intputs(sustained_hits_entry.get())

    if balistic_or_weapon_skill_entry.get() == "":
        balistic_skill = None
    else:
        balistic_skill = clamp_value_to_dice_range(
            int(balistic_or_weapon_skill_entry.get())
        )
    attack_str = int(attack_str_entry.get())
    target_toughness = int(toughness_entry.get())
    AP = abs(int(weapon_AP_entry.get()))
    save = int(save_entry.get())
    enemy_wounds = int(wound_per_model_entry.get())
    wound_mod = int(wound_mod_entry.get())
    hit_mod = int(hit_mod_entry.get())

    if invuln_save_entry.get() != "":
        target_invuln = int(invuln_save_entry.get())
    else:
        target_invuln = 10

    save_mod = int(save_mod_entry.get())

    if FNP_entry.get() == "":
        FNP = None
    else:
        FNP = clamp_value_to_dice_range(int(FNP_entry.get()))

    crit_hit = clamp_value_to_dice_range(int(crit_hits_entry.get()))
    crit_wound = clamp_value_to_dice_range(int(crit_wound_entry.get()))

    hits, wounds, not_saved, dmg, models = get_average_dmg_for_weapon_profile(
        attacks_val,
        balistic_skill,
        attack_str,
        target_toughness,
        dmg_val,
        AP,
        save,
        enemy_wounds,
        wound_rerolls=reroll_lookup[wound_rerolls.get()],
        wound_modifer=wound_mod,
        hit_rerolls=reroll_lookup[hit_rerolls.get()],
        hit_modifier=hit_mod,
        target_invuln=target_invuln,
        save_modifier=save_mod,
        save_rerolls=reroll_lookup[save_rerolls.get()],
        has_cover=var_cover.get(),
        target_FNP=FNP,
        sustained_hits=sustained_val,
        has_lethal_hits=var_lethal_hits.get(),
        has_dev_wounds=var_dev_wounds.get(),
        crit_hit_on=crit_hit,
        crit_wound_on=crit_wound,
        dmg_dice=dmg_dice,
        attacks_dice=attacks_dice,
        sustained_hits_dice=sustained_dice,
    )

    output_text.delete(1.0, tk.END)  # Clear previous output
    output_text.insert(tk.END, f"Average Hits: {hits:.2f}\n")
    output_text.insert(tk.END, f"Average Wounds: {wounds:.2f}\n")
    output_text.insert(tk.END, f"Average Unsaved: {not_saved:.2f}\n")
    output_text.insert(tk.END, f"Average Damage: {dmg:.2f}\n")
    output_text.insert(tk.END, f"Average Models Killed: {models:.2f}\n")


def validate_numeric(char, entry_value, entry_widget):
    if (
        char.isdigit()
        or char == ""
        or char == "-"
        or (char == "\x08" and not entry_value)
    ):
        entry_widget.config(bg="white")
        return True
    else:
        entry_widget.config(bg="pink")
        return False


def validate_numeric_or_dice(char, entry_value, entry_widget):
    if (
        char.isdigit()
        or char == ""
        or char == "d"
        or char == "+"
        or char == " "
        or (char == "\x08" and not entry_value)
    ):
        entry_widget.config(bg="white")
        return True
    else:
        entry_widget.config(bg="pink")
        return False


# Create the main window
root = tk.Tk()
root.title("Warhammer Calculator")

# Event Binding

main_frame = tk.Frame(root, borderwidth=1, relief="ridge")
main_frame.pack(fill="both", expand=True)

# Create Attack Stats Frame
attack_frame = tk.Frame(main_frame, borderwidth=2, relief="ridge")
attack_frame.pack(side="top", fill="both", expand=True)

# Create Attack Stats input fields
attacks_label = tk.Label(attack_frame, text="Number of Attacks:")
attacks_label.pack(side="top", fill="both", expand=True)
attacks_entry = tk.Entry(attack_frame)
attacks_entry.pack(side="top", fill="both", expand=True)

attacks_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=attacks_entry: validate_numeric_or_dice(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
attacks_entry.config(validate="key", validatecommand=attacks_input_CMD)

balistic_or_weapon_skill_label = tk.Label(
    attack_frame, text="Ballistic or Weapon Skill:"
)
balistic_or_weapon_skill_label.pack(side="top", fill="both", expand=True)
balistic_or_weapon_skill_entry = tk.Entry(attack_frame)
balistic_or_weapon_skill_entry.pack(side="top", fill="both", expand=True)

balistic_or_weapon_skill_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=balistic_or_weapon_skill_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
balistic_or_weapon_skill_entry.config(
    validate="key", validatecommand=balistic_or_weapon_skill_CMD
)

attack_str_label = tk.Label(attack_frame, text="Attack Strength:")
attack_str_label.pack(side="top", fill="both", expand=True)
attack_str_entry = tk.Entry(attack_frame)
attack_str_entry.pack(side="top", fill="both", expand=True)

attack_str_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=attack_str_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
attack_str_entry.config(validate="key", validatecommand=attack_str_input_CMD)

weapon_AP_label = tk.Label(attack_frame, text="Weapon AP:")
weapon_AP_label.pack(side="top", fill="both", expand=True)
weapon_AP_entry = tk.Entry(attack_frame)
weapon_AP_entry.pack(side="top", fill="both", expand=True)

validate_AP_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=weapon_AP_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
weapon_AP_entry.config(validate="key", validatecommand=validate_AP_input_CMD)

weapon_dmg_label = tk.Label(attack_frame, text="Weapon Damage:")
weapon_dmg_label.pack(side="top", fill="both", expand=True)
weapon_dmg_entry = tk.Entry(attack_frame)
weapon_dmg_entry.pack(side="top", fill="both", expand=True)

weapon_dmg_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=weapon_dmg_entry: validate_numeric_or_dice(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
weapon_dmg_entry.config(validate="key", validatecommand=weapon_dmg_CMD)

# Create Hit Frame
hit_frame = tk.Frame(main_frame, borderwidth=2, relief="ridge")
hit_frame.pack(side="top", fill="both", expand=True)

# Create Hit input fields
hit_mod_label = tk.Label(hit_frame, text="Hit Modifier:")
hit_mod_label.pack(side="top", fill="both", expand=True)
hit_mod_entry = tk.Entry(hit_frame)
hit_mod_entry.pack(side="top", fill="both", expand=True)
hit_mod_entry.insert(0, "0")

validate_hit_mod_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=hit_mod_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
hit_mod_entry.config(validate="key", validatecommand=validate_hit_mod_input_CMD)

sustained_hits_label = tk.Label(hit_frame, text="Sustained Hits:")
sustained_hits_label.pack(side="top", fill="both", expand=True)
sustained_hits_entry = tk.Entry(hit_frame)
sustained_hits_entry.pack(side="top", fill="both", expand=True)
sustained_hits_entry.insert(0, "0")

validate_sustained_hits_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=sustained_hits_entry: validate_numeric_or_dice(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
sustained_hits_entry.config(validate="key", validatecommand=validate_sustained_hits_CMD)

crit_hits_label = tk.Label(hit_frame, text="Critical Hit:")
crit_hits_label.pack(side="top", fill="both", expand=True)
crit_hits_entry = tk.Entry(hit_frame)
crit_hits_entry.pack(side="top", fill="both", expand=True)
crit_hits_entry.insert(0, "6")

validate_crit_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=crit_hits_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
crit_hits_entry.config(validate="key", validatecommand=validate_crit_input_CMD)

var_lethal_hits = tk.BooleanVar()
lethal_hits_checkbox = tk.Checkbutton(
    hit_frame, text="Lethal Hits", variable=var_lethal_hits
)
lethal_hits_checkbox.pack(side="top", fill="both", expand=True)

hit_rerolls_label = tk.Label(hit_frame, text="Hit Rerolls:")
hit_rerolls_label.pack(side="top", fill="both", expand=True)
hit_rerolls = ttk.Combobox(hit_frame, values=rerolls)
hit_rerolls.pack(side="top", fill="both", expand=True)
hit_rerolls.set("None")

# Create Wound Frame
wound_frame = tk.Frame(main_frame, borderwidth=2, relief="ridge")
wound_frame.pack(side="top", fill="both", expand=True)

# Create Wound input fields
wound_mod_label = tk.Label(wound_frame, text="Wound Modifier:")
wound_mod_label.pack(side="top", fill="both", expand=True)
wound_mod_entry = tk.Entry(wound_frame)
wound_mod_entry.pack(side="top", fill="both", expand=True)
wound_mod_entry.insert(0, "0")

validate_wound_mod_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=wound_mod_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
wound_mod_entry.config(validate="key", validatecommand=validate_wound_mod_input_CMD)

crit_wound_label = tk.Label(wound_frame, text="Critical Wound:")
crit_wound_label.pack(side="top", fill="both", expand=True)
crit_wound_entry = tk.Entry(wound_frame)
crit_wound_entry.pack(side="top", fill="both", expand=True)
crit_wound_entry.insert(0, "6")

validate_crit_wound_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=crit_wound_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
crit_wound_entry.config(validate="key", validatecommand=validate_crit_wound_input_CMD)

var_dev_wounds = tk.BooleanVar()
dev_wounds_checkbox = tk.Checkbutton(
    wound_frame, text="Devastating Wounds", variable=var_dev_wounds
)
dev_wounds_checkbox.pack(side="top", fill="both", expand=True)

wound_rerolls_label = tk.Label(wound_frame, text="Wound Rerolls:")
wound_rerolls_label.pack(side="top", fill="both", expand=True)
wound_rerolls = ttk.Combobox(wound_frame, values=rerolls)
wound_rerolls.pack(side="top", fill="both", expand=True)
wound_rerolls.set("None")

# Create Defense Frame
defense_frame = tk.Frame(main_frame, borderwidth=2, relief="ridge")
defense_frame.pack(side="top", fill="both", expand=True)

# Create Defense input fields
toughness_label = tk.Label(defense_frame, text="Toughness:")
toughness_label.pack(side="top", fill="both", expand=True)
toughness_entry = tk.Entry(defense_frame)
toughness_entry.pack(side="top", fill="both", expand=True)

validate_toughness_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=toughness_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
toughness_entry.config(validate="key", validatecommand=validate_toughness_input_CMD)

save_label = tk.Label(defense_frame, text="Save:")
save_label.pack(side="top", fill="both", expand=True)
save_entry = tk.Entry(defense_frame)
save_entry.pack(side="top", fill="both", expand=True)

validate_save_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=save_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
save_entry.config(validate="key", validatecommand=validate_save_input_CMD)

save_mod_label = tk.Label(defense_frame, text="Save Modifier:")
save_mod_label.pack(side="top", fill="both", expand=True)
save_mod_entry = tk.Entry(defense_frame)
save_mod_entry.pack(side="top", fill="both", expand=True)
save_mod_entry.insert(0, "0")

validate_save_mod_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=save_mod_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
save_mod_entry.config(validate="key", validatecommand=validate_save_mod_input_CMD)

invuln_save_label = tk.Label(defense_frame, text="Invulnerable Save:")
invuln_save_label.pack(side="top", fill="both", expand=True)
invuln_save_entry = tk.Entry(defense_frame)
invuln_save_entry.pack(side="top", fill="both", expand=True)

validate_invuln_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=invuln_save_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
invuln_save_entry.config(validate="key", validatecommand=validate_invuln_input_CMD)

wound_per_model_label = tk.Label(defense_frame, text="Wounds Per Model:")
wound_per_model_label.pack(side="top", fill="both", expand=True)
wound_per_model_entry = tk.Entry(defense_frame)
wound_per_model_entry.pack(side="top", fill="both", expand=True)

validate_wounds_per_model_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=wound_per_model_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
wound_per_model_entry.config(
    validate="key", validatecommand=validate_wounds_per_model_input_CMD
)

FNP_label = tk.Label(defense_frame, text="Feel No Pain:")
FNP_label.pack(side="top", fill="both", expand=True)
FNP_entry = tk.Entry(defense_frame)
FNP_entry.pack(side="top", fill="both", expand=True)

validate_FNP_input_CMD = (
    main_frame.register(
        lambda char, entry_value, entry=FNP_entry: validate_numeric(
            char, entry_value, entry
        )
    ),
    "%S",
    "%P",
)
FNP_entry.config(validate="key", validatecommand=validate_FNP_input_CMD)

var_cover = tk.BooleanVar()
cover_checkbox = tk.Checkbutton(defense_frame, text="Cover", variable=var_cover)
cover_checkbox.pack(side="top", fill="both", expand=True)
save_rerolls_label = tk.Label(defense_frame, text="Save Rerolls:")
save_rerolls_label.pack(side="top", fill="both", expand=True)
save_rerolls = ttk.Combobox(defense_frame, values=rerolls)
save_rerolls.pack(side="top", fill="both", expand=True)
save_rerolls.set("None")

# Create confirm button

button_frame = tk.Frame(main_frame, borderwidth=2, relief="ridge")
button_frame.pack(side="top", fill="both", expand=True)

confirm_button = tk.Button(button_frame, text="Average", command=on_confirm_button)
confirm_button.pack(side="left", fill="both", expand=True)

number_of_sims = tk.Entry(button_frame)
number_of_sims.pack(side="left", fill="both", expand=True)
number_of_sims.insert(0, "1")

simulate_button = tk.Button(button_frame, text="Simulate", command=on_simulate_button)
simulate_button.pack(side="left", fill="both", expand=True)

# Create output area
output_text = tk.Text(main_frame, height=8, width=30)
output_text.pack(side="top", fill="both", expand=True)

# Start the Tkinter event loop
root.mainloop()
