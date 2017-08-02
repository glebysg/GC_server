// JavaScript Document
function thermometer(goalAmount, progressAmount, animate) {
    "use strict";
    var $thermo = $("#thermometer"),
        $progress = $(".progress", $thermo),
        $goal = $(".goal", $thermo),
        percentageAmount;

    goalAmount = goalAmount || parseFloat($goal.text()),
    progressAmount = progressAmount || parseFloat($progress.text()),
    percentageAmount = Math.min(Math.round(progressAmount / goalAmount * 1000) / 10, 100); //make sure we have 1 decimal point

    $goal.find(".amount").text();
    $progress.find(".amount").text();

    $progress.find(".amount").hide();
    if (animate !== false) {
        $progress.animate({
            "height": percentageAmount + "%"
        }, 1200, function () {
            $(this).find(".amount").fadeIn(200);
        });
    } else {
        $progress.css({
            "height": percentageAmount + "%"
        });
        $progress.find(".amount").fadeIn(200);
    }
}

$(document).ready(function () {

    thermometer();
   
});