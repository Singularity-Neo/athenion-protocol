// GENKI NETWORK SMART CONTRACT - V1.0 (SOLANA ANCHOR)
// Goal: 1 Billion $GENKI with built-in Burn and Swarm Reward mechanisms.

use anchor_lang::prelude::*;
use anchor_spl::token::{self, Mint, Token, TokenAccount, Transfer};

declare_id!("GenkiToken1111111111111111111111111111111111"); // Placeholder, will change on deploy

#[program]
pub mod genki_network {
    use super::*;

    /// Initialize the $GENKI Token with 1 Billion Supply
    pub fn initialize_genki(ctx: Context<InitializeGenki>) -> Result<()> {
        msg!("Genki Network: Vital Energy Token Initialized.");
        msg!("Total Supply: 1,000,000,000 $GENKI");
        Ok(())
    }

    /// Transfer with Automatic Burn (0.5% Burn + 0.5% Reward Pool)
    pub fn transfer_vital_energy(ctx: Context<TransferVital>, amount: u64) -> Result<()> {
        let burn_amount = amount / 200; // 0.5%
        let reward_amount = amount / 200; // 0.5%
        let final_amount = amount - burn_amount - reward_amount;

        // 1. Burn the tokens (Remove from supply)
        let cpi_accounts_burn = token::Burn {
            mint: ctx.accounts.mint.to_account_info(),
            from: ctx.accounts.from.to_account_info(),
            authority: ctx.accounts.authority.to_account_info(),
        };
        let cpi_ctx_burn = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts_burn);
        token::burn(cpi_ctx_burn, burn_amount)?;

        // 2. Send to Reward Pool (For Swarm/Workers)
        let cpi_accounts_reward = token::Transfer {
            from: ctx.accounts.from.to_account_info(),
            to: ctx.accounts.reward_pool.to_account_info(),
            authority: ctx.accounts.authority.to_account_info(),
        };
        let cpi_ctx_reward = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts_reward);
        token::transfer(cpi_ctx_reward, reward_amount)?;

        // 3. Complete User Transfer
        let cpi_accounts_final = token::Transfer {
            from: ctx.accounts.from.to_account_info(),
            to: ctx.accounts.to.to_account_info(),
            authority: ctx.accounts.authority.to_account_info(),
        };
        let cpi_ctx_final = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts_final);
        token::transfer(cpi_ctx_final, final_amount)?;

        msg!("Vital Energy Circulated. Burned: {}, Final: {}", burn_amount, final_amount);
        Ok(())
    }
}

#[derive(Accounts)]
pub struct InitializeGenki<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct TransferVital<'info> {
    #[account(mut)]
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub from: Account<'info, TokenAccount>,
    #[account(mut)]
    pub to: Account<'info, TokenAccount>,
    #[account(mut)]
    pub reward_pool: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>,
}
