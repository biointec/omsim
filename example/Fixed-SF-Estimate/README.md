This example show cases the setting fixed_stretch_factor_estimate introduced in v1.1.20.

The XML example-auto-chip-sf.xml shows the default behaviour (fixed_stretch_factor_estimate = 0): chip SF is perfectly "estimated", this is the same behaviour as in earlier OMSim versions.
The XML fixed-auto-chip-sf.xml shows the new behaviour: the chip SF is "estimated" as given by the setting fixed_stretch_factor_estimate = 0.85. If the actual chip SF is larger than 0.85, this will result in a BNX file where the positions are upscaled.

If you want to use the predetermined fixed_stretch_factor_estimate, then setting this equal to the average stretch_factor setting seems reasonable. This corresponds with knowing the average SF of chips, but no estimate of per chip SF is made.