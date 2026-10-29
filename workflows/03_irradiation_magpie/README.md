# Track C: irradiation-coupled corrosion (exploratory)

Goal: add an irradiation-induced defect source to the corrosion model and test whether vacancy/interstitial supersaturation explains the proton-irradiation effects reported by Zhou et al. (Nat. Commun. 2020; Ni-Cr slowed) and AlMousa et al. (2023; Fe-based accelerated).

Pieces already in your uploads:

- `magpie` has MyTRIM (binary-collision ion transport) coupling to MOOSE, plus `grand_potential_magpie` and `nrt_comparison` examples. Start there to produce a damage-rate field (dpa/s, Frenkel pairs/um^3/s).  
- `mesoscale_molten_salt_model` has the grand-potential corrosion inputs. The vacancy variable c\_v is already implicit (c\_v \= 1 \- c\_Ni \- c\_Cr); the open design question is whether to make it an independent field with source/sink terms at GBs and the surface.

Milestones

1. Build Magpie against the same MOOSE version used by the corrosion inputs; run `nrt_comparison`.  
2. Convert MyTRIM damage profile (proton, \~MeV, Ni) into a 1D source S(x) in defects/um^3/s.  
3. Add a vacancy-enhanced diffusivity D\_Cr(c\_v) and GB sink term to the 1D input; compare against the non-irradiated 1D baseline and Zhou 2020 depth data.  
4. Only after 1-3 work: 2D with grains.IMPORTANT: Bhave & Tonks (2025) state they are *already adding radiation* to the model. Ask before investing here; this track may be best framed as joint work rather than parallel work.