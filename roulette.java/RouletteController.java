package com.example.roulette.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Random;

@Controller
public class RouletteController {
    private int balance = 100; // Initial balance

    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("balance", balance);
        model.addAttribute("result", "-");
        model.addAttribute("message", "");
        return "index"; // Returns the template name to render
    }

    @PostMapping("/spin")
    public String spin(@RequestParam int bet, @RequestParam int wager, Model model) {
        Random random = new Random();
        int result = random.nextInt(37); // Spin results between 0 and 36

        String message;
        if (bet < 0 || bet > 36) {
            message = "Invalid bet. Please enter a number between 0 and 36.";
        } else if (wager <= 0 || wager > balance) {
            message = "Invalid wager. Please enter a valid amount.";
        } else {
            balance -= wager; // Deduct wager from balance
            if (result == bet) {
                message = "You win! You earned $" + (wager * 35) + ".";
                balance += wager * 35; // Calculate winnings
            } else {
                message = "You lose.";
            }

            if (balance <= 0) {
                message = "You've run out of money! Game over!";
            }
        }

        model.addAttribute("balance", balance);
        model.addAttribute("result", result);
        model.addAttribute("message", message);
        return "index"; // Returns the template to render with updated data
    }
}