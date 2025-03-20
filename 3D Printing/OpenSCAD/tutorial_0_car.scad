// RESOLUTION SETTINGS
$fa = 1;
$fs = 0.4;

// CAR BODY
scale([1.2, 1, 1])
{
	// BASE
	cube([60, 20, 10], center = true);
	// TOP
	translate([5, 0, 10 - 0.01])
		cube([30, 20, 10], center = true);
}

// WHEELS
// FRONT LEFT
translate([-20, -15, 0])
	rotate([90, 0, 0])
		cylinder(h = 3, r = 8, center = true);
// FRONT RIGHT
translate([-20, 15, 0])
	rotate([90, 0, 0])
		cylinder(h = 3, r = 8, center = true);
// REAR RIGHT
translate([20, 15, 0])
	rotate([90, 0, 0])
		cylinder(h = 3, r = 8, center = true);
// REAR LEFT
translate([20, -15, 0])
	rotate([90, 0, 0])
		cylinder(h = 3, r = 8, center = true);

// AXLES
// FRONT
translate([-20, 0, 0])
	rotate([90, 0, 0])
		cylinder(h = 30, r = 2, center = true);
// REAR
translate([20, 0, 0])
	rotate([90, 0, 0])
		cylinder(h = 30, r = 2, center = true);