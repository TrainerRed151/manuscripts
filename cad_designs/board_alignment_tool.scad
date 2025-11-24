// Parameters
$fn = 200;
round_over = 2; //mm

spine_gap = 9.5 - 2*round_over; //mm
spine_leg = 150 - 2*round_over; //mm

back_width = 9.5 - 2*round_over; //mm
back_length = 200 - 2*round_over; //mm

guide_depth = 12 - 2*round_over; //mm


// Spine
translate([0, -spine_gap/2, 0]) {
    minkowski() {
        cube([spine_leg, spine_gap, guide_depth]);
        sphere(round_over);
    }
}

// Back
translate([-back_width, -back_length/2, 0]) {
    minkowski() {
        cube([back_width, back_length, guide_depth]);
        sphere(round_over);
    }
}